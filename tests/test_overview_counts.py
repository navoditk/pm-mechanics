"""The "At a glance" table in docs/OVERVIEW.md, checked against the tree.

Auditing rule 10 says a count in a doc is a claim and drifts whenever content
is added. Nothing enforced it, so the table drifted: it advertised 211 tests
when there were 263, and 1,640 lines of analytics when there were 1,796. The
artifact preview embeds this page, so the stale numbers were published too.

These read the live tree rather than restating the figures, so the test
cannot drift in the same direction as the document it guards.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERVIEW = ROOT / "docs" / "OVERVIEW.md"


def cell(label: str) -> str:
    """The right-hand cell of the `| label | value |` row."""
    match = re.search(
        rf"^\|\s*{re.escape(label)}\s*\|\s*(.+?)\s*\|\s*$",
        OVERVIEW.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    assert match, f"no '{label}' row in the At a glance table"
    return match.group(1)


def first_int(text: str) -> int:
    match = re.search(r"([\d,]+)", text)
    assert match, f"no number in {text!r}"
    return int(match.group(1).replace(",", ""))


def test_test_count_matches_the_suite():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    collected = int(re.search(r"(\d+) tests collected", result.stdout).group(1))
    assert first_int(cell("Tests")) == collected


def test_test_file_count_matches():
    claimed = int(re.search(r"(\d+) test files", cell("Tests")).group(1))
    assert claimed == len(list((ROOT / "tests").glob("test_*.py")))


def test_analytics_module_and_line_counts_match():
    files = sorted((ROOT / "src" / "pm").rglob("*.py"))
    lines = sum(len(f.read_text(encoding="utf-8").splitlines()) for f in files)
    claim = cell("Analytics code")
    assert first_int(claim) == lines
    assert int(re.search(r"(\d+) modules", claim).group(1)) == len(files)


def test_notebook_count_matches_what_is_tracked():
    tracked = subprocess.run(
        ["git", "ls-files", "*.ipynb"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.split()
    assert first_int(cell("Notebooks")) == len(tracked)


def test_reference_page_count_matches():
    assert first_int(cell("Reference pages")) == len(list((ROOT / "reference").rglob("*.md")))


def test_use_case_count_matches_the_taxonomy():
    sys.path.insert(0, str(ROOT / "scripts"))
    from reference_taxonomy import USE_CASES

    assert first_int(cell("Use-case workflows")) == len(USE_CASES)


def test_the_skills_row_does_not_claim_a_single_tool():
    """The skills carry loaders for all three agents; saying otherwise sends
    Copilot and Codex readers away from tutoring that works for them."""
    row = cell("Learning skills")
    for skill in ("pmexpert", "tutor", "pm-query"):
        assert skill in row
    assert "Copilot" in row and "Codex" in row
