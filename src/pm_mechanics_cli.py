"""The repository's front door: one routed command instead of seven script paths.

`scripts/` holds seven entry points and the README names none of them, so what
this repository can do is discoverable only by listing the directory. This
module is the console script declared in `pyproject.toml`; every subcommand
delegates to the module that already does the work.

Commands are grouped by who they are for, because the two audiences want
different things:

- **Learner commands** (`topics`, `reference`, `progress`) navigate the
  reference library and the mastery ledger. They are read-only and need no
  model, network, or API key.
- **Developer commands** (`check`) serve someone maintaining the repository.

The interactive teaching itself lives in the skills -- say `pmexpert`,
`tutor`, or `pm-query` to a coding agent -- because deriving a formula with a
learner is a conversation, not a command. This CLI is the map; the skills are
the lesson.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
MASTERY = REPO_ROOT / "docs/mastery.md"

CHECKS: tuple[tuple[str, list[str]], ...] = (
    ("lint", ["ruff", "check", "src", "tests", "scripts"]),
    ("format", ["ruff", "format", "--check", "src", "tests", "scripts"]),
    ("repo structure", ["python", "scripts/check_repo.py"]),
    ("doc links", ["python", "scripts/check_doc_links.py"]),
    ("tests", ["pytest", "-q"]),
)

OVERVIEW = """\
pm-mechanics -- a build-first portfolio-management mechanics trainer

Learning (read-only; no model, network, or API key needed)
  topics [SECTION]   list the reference library, or one section of it
  reference PAGE     print one reference page
  progress           your mastery ladder, from docs/mastery.md

Development
  check              run the same gates CI runs

The interactive teaching lives in the skills, not here. Open this checkout in
Claude Code, GitHub Copilot, or Codex and say:

  pmexpert     the guided mastery path, rung by rung
  tutor        a per-topic tutor persona
  pm-query     ask the analytics library a question in plain English

Deriving a formula with a learner is a conversation, not a command -- this CLI
is the map, the skills are the lesson.
"""


def _taxonomy():
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import reference_taxonomy

    return reference_taxonomy


def cmd_topics(args: argparse.Namespace) -> int:
    taxonomy = _taxonomy()
    wanted = (args.section or "").lower()
    shown = 0
    for name, _meta, pages in taxonomy.SECTIONS:
        if wanted and wanted not in name.lower():
            continue
        shown += 1
        print(f"\n{name}")
        for path, title in pages:
            print(f"  {path:<52} {title}")
    if not shown:
        print(f"No section matching {args.section!r}.", file=sys.stderr)
        print(
            "Sections: " + ", ".join(name for name, _, _ in taxonomy.SECTIONS),
            file=sys.stderr,
        )
        return 1
    if not wanted:
        print(f"\n{len(taxonomy.TITLES)} pages. Read one with: pm-mechanics reference <path>")
    return 0


def cmd_reference(args: argparse.Namespace) -> int:
    taxonomy = _taxonomy()
    page = args.page.removeprefix("reference/")
    if page not in taxonomy.TITLES:
        matches = [p for p in taxonomy.TITLES if page.rstrip(".md") in p]
        print(f"No reference page {args.page!r}.", file=sys.stderr)
        if matches:
            print("Did you mean:", file=sys.stderr)
            for match in matches[:5]:
                print(f"  {match}", file=sys.stderr)
        return 1
    print((REPO_ROOT / "reference" / page).read_text(encoding="utf-8"))
    return 0


def cmd_progress(_: argparse.Namespace) -> int:
    """Summarise the mastery ledger rather than reprinting 92 rows."""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    import mastery_rules

    # Parsed by field rather than by a guessed row shape: the ledger's columns
    # are Concept | Reference page | Status | Rungs | XP | Last session, and
    # the Rungs cell is the only one that is exactly four rung characters.
    rows: list[tuple[str, str]] = []
    for line in MASTERY.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rungs = next(
            (c for c in cells if re.fullmatch(r"[DABE·]{4}", c)),
            None,
        )
        if rungs and cells[0] and cells[0] != "Concept":
            rows.append((cells[0], rungs))
    if not rows:
        print("No mastery rows found in docs/mastery.md.", file=sys.stderr)
        return 1

    confirmed = sum(1 for _, rungs in rows if mastery_rules.status_for(rungs) == "confirmed")
    started = sum(1 for _, rungs in rows if rungs != mastery_rules.NOT_CLEARED * 4)
    level = mastery_rules.level_for(confirmed, len(rows))

    print(f"Level: {level}")
    print(f"Confirmed: {confirmed} of {len(rows)} topics")
    print(f"Started:   {started} of {len(rows)}")
    print("\nIn progress:")
    any_partial = False
    for topic, rungs in rows:
        if (
            rungs != mastery_rules.NOT_CLEARED * 4
            and mastery_rules.status_for(rungs) != "confirmed"
        ):
            any_partial = True
            nxt = mastery_rules.next_rung(rungs)
            print(f"  {rungs}  {topic:<44} next: {nxt}")
    if not any_partial:
        print("  (nothing part-way through)")
    print("\nAdvance one with: say `pmexpert` to a coding agent in this checkout.")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    selected = CHECKS[:2] if args.fast else CHECKS
    failed = []
    for name, command in selected:
        print(f"-- {name} ", end="", flush=True)
        result = subprocess.run(
            [".venv/bin/" + command[0], *command[1:]],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print("ok")
        else:
            print("FAILED")
            failed.append(name)
            sys.stdout.write(result.stdout[-2000:])
            sys.stderr.write(result.stderr[-2000:])
            if not args.keep_going:
                break
    if failed:
        print(f"\n{len(failed)} check(s) failed: {', '.join(failed)}")
        return 1
    print(f"\nAll {len(selected)} checks passed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pm-mechanics",
        description="A build-first portfolio-management mechanics trainer.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    topics = sub.add_parser("topics", help="list the reference library")
    topics.add_argument("section", nargs="?", help="filter to one section")
    topics.set_defaults(func=cmd_topics)

    reference = sub.add_parser("reference", help="print one reference page")
    reference.add_argument("page", help="e.g. fixed_income/duration.md")
    reference.set_defaults(func=cmd_reference)

    progress = sub.add_parser("progress", help="your mastery ladder")
    progress.set_defaults(func=cmd_progress)

    check = sub.add_parser("check", help="run the gates CI runs (developer)")
    check.add_argument("--fast", action="store_true", help="lint and format only")
    check.add_argument("--keep-going", action="store_true", help="do not stop at first failure")
    check.set_defaults(func=cmd_check)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    if not getattr(args, "command", None):
        print(OVERVIEW, end="")
        raise SystemExit(0)
    raise SystemExit(args.func(args))
