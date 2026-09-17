"""Stage this repo's documentation content into site_src/ for MkDocs.

Mirrors each source directory's real relative path under site_src/, so
the existing relative markdown links between pages (e.g. "../ROADMAP.md",
"./mastery-guide.md") keep resolving correctly without any rewriting.
site_src/ and the built site/ are both gitignored build artifacts -
regenerate with this script, never edit site_src/ directly.

Run: python scripts/build_docs_site.py
Then: mkdocs build   (or mkdocs serve, for local preview)
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "site_src"

TOP_LEVEL_FILES = ["README.md", "ROADMAP.md", "AGENTS.md", "SDLC.md", "SETUP.md"]
TOP_LEVEL_DIRS = ["reference", "curriculum", "notebooks", "use_cases", "tutors", "resources", "docs"]

HOMEPAGE = """# PM Mechanics

Public, read-only mirror of the
[pm-mechanics](https://github.com/navoditk/pm-mechanics) curriculum — browse
the entire material without cloning the repo. This site rebuilds
automatically from `main` on every push.

A mechanics trainer, not a desk-grade risk system: no live market data, no
production curve or optimization engine. The unit of work is a formula made
concrete, unit-aware, and tested.

For the interactive version — running the tests, `/pmexpert`, `/tutor`,
`/pm-query` — clone the repo instead; see
[Getting started](docs/getting-started.md).

## Where to start

- **[Repository overview](docs/OVERVIEW.md)** — what's here, how deep it
  goes, and what's still conceptual-only
- **[Mastery guide](docs/mastery-guide.md)** — how the interactive
  `/pmexpert` trainer works (only usable once you've cloned the repo)
- **[Learning paths](docs/learning-paths.md)** — choose a route by goal
- **[Reference index](reference/index.md)** — every concept and
  instrument page, by topic
- **[Curriculum](curriculum/bootcamp_01_foundations/README.md)** — the
  14-day bootcamp, day by day
- **[Use cases](use_cases/index.md)** — realistic portfolio workflows

There's also a lighter, single-page
[Artifact preview](https://claude.ai/code/artifact/902379a8-c198-4970-aca8-4cb71e2a3d5c)
covering the reference pages, curriculum, and use cases — useful if this
site isn't reachable. It's refreshed manually rather than on every push;
this site is the always-current one.

## Related repositories

This repo is the math layer: the deterministic analytics and the curriculum
that teaches you to derive them.
[agentic-pm-lab](https://github.com/navoditk/agentic-pm-lab) is the agent
layer built on the same domain — how to let an LLM call analytics like these
without it inventing the numbers, using LangGraph/Deep Agents, Cedar
authorization, evaluation, OpenTelemetry, MCP, and AWS Bedrock AgentCore.

Read them in that order. This repo answers "what is DV01, and how do I
compute it correctly?"; agentic-pm-lab answers "how do I put a DV01 tool
behind an agent and still trust the answer?" See
[ROADMAP](ROADMAP.md)'s Phase 12 for where the two meet.
"""


def clean():
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)


def copy_content():
    for name in TOP_LEVEL_FILES:
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, STAGE / name)
    for name in TOP_LEVEL_DIRS:
        src = ROOT / name
        if src.exists():
            shutil.copytree(
                src,
                STAGE / name,
                ignore=shutil.ignore_patterns("__pycache__", "*.json"),
            )


def write_homepage():
    # Written as README.md, not index.md: mkdocs treats a directory's
    # README.md as its index page automatically, and writing both would
    # collide (mkdocs would silently drop README.md, breaking every
    # other page's real "../README.md" link back to it).
    (STAGE / "README.md").write_text(HOMEPAGE)


def main():
    clean()
    copy_content()
    write_homepage()
    print(f"Staged docs site source at {STAGE}")


if __name__ == "__main__":
    main()
