"""The console script, tested as the front door a new reader actually types.

The behaviours worth pinning are the ones someone notices: an unknown name
produces a readable error and a non-zero status rather than a traceback, the
advertised commands exist, and `progress` reads the real ledger rather than a
guessed row shape -- the first version of it matched columns that do not
exist and reported "no mastery rows found" against a populated file.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from pm_mechanics_cli import (
    CHECKS,
    OVERVIEW,
    build_parser,
    cmd_progress,
    cmd_reference,
    cmd_topics,
)


def parse(argv):
    return build_parser().parse_args(argv)


# --- the advertised surface exists -------------------------------------------


@pytest.mark.parametrize("command", ["topics", "reference", "progress", "check"])
def test_every_advertised_command_parses(command):
    assert command in OVERVIEW
    assert parse([command, "x"] if command == "reference" else [command])


def test_the_overview_separates_learner_from_developer_commands():
    assert "Learning" in OVERVIEW and "Development" in OVERVIEW
    learning, development = OVERVIEW.split("Development", 1)
    assert "topics" in learning and "progress" in learning
    assert "check" in development


def test_the_overview_points_at_the_skills_for_teaching():
    """The CLI is the map; the skills are the lesson. Say so, or a reader
    assumes a navigation tool is all the repository offers."""
    for skill in ("pmexpert", "tutor", "pm-query"):
        assert skill in OVERVIEW


# --- topics and reference -----------------------------------------------------


def test_topics_lists_the_whole_library_by_default(capsys):
    assert cmd_topics(parse(["topics"])) == 0
    out = capsys.readouterr().out
    assert "Fixed Income" in out
    assert "fixed_income/duration.md" in out


def test_topics_filters_to_one_section(capsys):
    assert cmd_topics(parse(["topics", "fixed income"])) == 0
    out = capsys.readouterr().out
    assert "fixed_income/duration.md" in out
    assert "concepts/sharpe_ratio.md" not in out


def test_an_unknown_section_lists_the_ones_that_exist(capsys):
    assert cmd_topics(parse(["topics", "not-a-section"])) == 1
    err = capsys.readouterr().err
    assert "Sections:" in err


def test_reference_prints_a_page(capsys):
    assert cmd_reference(parse(["reference", "fixed_income/duration.md"])) == 0
    assert "Duration" in capsys.readouterr().out


def test_reference_accepts_the_path_with_or_without_its_prefix(capsys):
    assert cmd_reference(parse(["reference", "reference/fixed_income/dv01.md"])) == 0
    assert "DV01" in capsys.readouterr().out


def test_an_unknown_page_suggests_near_matches(capsys):
    assert cmd_reference(parse(["reference", "duration"])) == 1
    err = capsys.readouterr().err
    assert "Did you mean" in err
    assert "duration" in err


# --- progress -----------------------------------------------------------------


def test_progress_reads_the_real_ledger(capsys):
    """Parsed by field, not by a guessed row shape.

    The ledger's columns are Concept | Reference page | Status | Rungs | XP |
    Last session. A first version assumed the rungs cell was second and found
    nothing at all in a fully populated file.
    """
    assert cmd_progress(parse(["progress"])) == 0
    out = capsys.readouterr().out
    assert "Level:" in out
    assert "of 86 topics" in out, "should agree with check_repo.py's own count"


def test_progress_agrees_with_the_repo_structure_check(capsys):
    """Two independent counts of the same table should match."""
    import re
    import subprocess

    cmd_progress(parse(["progress"]))
    from_cli = int(re.search(r"of (\d+) topics", capsys.readouterr().out).group(1))

    result = subprocess.run(
        [sys.executable, "scripts/check_repo.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    from_checker = int(re.search(r"(\d+) mastery rows", result.stdout).group(1))
    assert from_cli == from_checker


# --- check --------------------------------------------------------------------


def test_check_runs_the_same_gates_as_ci():
    """Drift between local `check` and CI is how "it passed locally" happens."""
    workflows = "\n".join(
        path.read_text(encoding="utf-8") for path in (ROOT / ".github/workflows").glob("*.yml")
    )
    for _, command in CHECKS:
        script = next((part for part in command if part.startswith("scripts/")), None)
        if script:
            assert script in workflows, f"{script} runs locally but not in CI"


def test_fast_is_a_strict_subset_of_the_full_gate_set():
    assert CHECKS[:2] != CHECKS
    assert all(check in CHECKS for check in CHECKS[:2])


# --- the tutor must be able to reach every page the library advertises -------


def _routed_reference_pages() -> set[str]:
    """Pages the tutor routing table can resolve.

    A bare filename in a cell inherits the directory of the previous full
    path in that same cell -- `reference/fixed_income/duration.md`, `dv01.md`
    -- so resolving them naively reports working rows as broken.
    """
    import re

    routed: set[str] = set()
    for line in (ROOT / "skills/tutor/SKILL.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        base = None
        for path in re.findall(r"`([^`]+)`", line):
            if not path.endswith(".md"):
                continue
            if "/" in path:
                base = str(Path(path).parent)
                routed.add(path.removeprefix("reference/"))
            elif base:
                routed.add(str(Path(base) / path).removeprefix("reference/"))
    return routed


def test_every_reference_page_has_a_tutor_route():
    """A page with no route is unreachable from `tutor`, however good it is.

    Two pages added in an earlier session -- backtesting biases and accrued
    interest/settlement -- were in the mastery ledger but had no routing row,
    so `pmexpert` could track them while `tutor` could not teach them.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    import reference_taxonomy

    unrouted = sorted(set(reference_taxonomy.TITLES) - _routed_reference_pages())
    assert not unrouted, f"reference pages with no tutor route: {unrouted}"


def test_every_routed_path_exists():
    """A route pointing at a moved file fails only when a learner tries it."""
    import re

    missing = []
    for line in (ROOT / "skills/tutor/SKILL.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "Persona" in line:
            continue
        base = None
        for path in re.findall(r"`([^`]+)`", line):
            if not re.search(r"\.(md|ipynb|py)$", path):
                continue
            if "/" in path:
                base = str(Path(path).parent)
                candidate = Path(path)
            else:
                candidate = Path(base) / path if base else Path(path)
            if not ((ROOT / candidate).exists() or (ROOT / "tutors" / path).exists()):
                missing.append(str(candidate))
    assert not missing, f"tutor routes pointing at missing files: {sorted(set(missing))}"
