# PM Mechanics

[![CI](https://github.com/navoditk/pm-mechanics/actions/workflows/ci.yml/badge.svg)](https://github.com/navoditk/pm-mechanics/actions/workflows/ci.yml)
[![Docs](https://github.com/navoditk/pm-mechanics/actions/workflows/docs.yml/badge.svg)](https://github.com/navoditk/pm-mechanics/actions/workflows/docs.yml)

A build-first portfolio-management mechanics trainer: the FICC and equity analytics behind portfolio construction, risk, optimization, fixed income, and equity work — derived, coded, and tested by hand rather than read about.

**A mechanics trainer, not a desk-grade risk system.** There are no live market-data feeds and no production-grade curve or optimization engine. The unit of work here is a formula made concrete, unit-aware, and tested — the median `src/pm` module is about 30 lines. [docs/OVERVIEW.md](docs/OVERVIEW.md) states exactly how deep each area goes and which topics are deliberately conceptual-only.

## Browse without cloning

- **[Docs site](https://navoditk.github.io/pm-mechanics/)** — the entire curriculum (every reference page, notebook, and use case) as a searchable static site, rebuilt automatically from `main` on every push
- **[Read-only preview](https://claude.ai/code/artifact/902379a8-c198-4970-aca8-4cb71e2a3d5c)** — a lighter, single-page version covering every reference page, the curriculum outline, and use cases, for a quick look or if the docs site above isn't reachable; refreshed on request rather than automatically

Either works without git, Python, or an account — for the interactive version (running tests, `/pmexpert`, `/tutor`, `/pm-query`), clone the repo instead.

## What this repo is

This repository is designed to support three modes at once:

1. Learn — structured curriculum and notebooks
2. Look up — reference pages, formulas, and code recipes
3. Apply — realistic portfolio-management use cases and analysis workflows

The goal is not just to read about PM concepts. The goal is to understand them deeply enough to reproduce them in code, test them, and explain them clearly.

## Start here

1. Read [docs/getting-started.md](docs/getting-started.md)
2. Review [docs/learning-paths.md](docs/learning-paths.md)
3. Choose a learning path from `curriculum/` or `reference/`
4. Open the matching notebook in `notebooks/`
5. Run the test suite and update progress in [docs/PROGRESS.md](docs/PROGRESS.md)

Prefer to be walked through it interactively instead of picking notebooks
yourself? Type `/pmexpert` and see
[docs/mastery-guide.md](docs/mastery-guide.md) — one command teaches the
whole curriculum, tracks progress, and picks up where you left off.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest -q
```

## Repository map

- `curriculum/` — bootcamps and structured learning tracks
- `reference/` — durable PM/FICC concept and instrument reference pages
- `notebooks/` — hands-on labs and worked examples
- `src/pm/` — reusable deterministic analytics library
- `tests/` — unit tests and correctness checks
- `use_cases/` — realistic portfolio workflows and scenario analysis
- `resources/` — curated external material and study references
- `tutors/` — tutor prompts and learning support
- `agents/` — agent workflows and operating instructions
- `templates/` — templates for new concepts, notebooks, and use cases
- `docs/` — canonical documentation hub for setup, workflow, and progress

## Related repositories

This repo is the **math layer**: the deterministic analytics and the curriculum
that teaches you to derive them.

[**agentic-pm-lab**](https://github.com/navoditk/agentic-pm-lab) is the **agent
layer** built on the same domain: how to let an LLM call analytics like these
without it inventing the numbers — LangGraph/Deep Agents, Cedar authorization,
evaluation, OpenTelemetry, MCP, and AWS Bedrock AgentCore.

Read them in that order. This repo answers *"what is DV01, and how do I compute
it correctly?"*; agentic-pm-lab answers *"how do I put a DV01 tool behind an
agent and still trust the answer?"* Phase 12 below is where the two meet.

## Core principles

- Financial logic must be documented, unit-aware, and tested
- Keep reusable calculations in `src/pm/`
- Preserve notebooks as teaching artifacts
- Prefer transparent, deterministic functions over opaque frameworks
- Do manual reasoning before relying on an agent

## Documentation

Use the docs hub as the canonical starting point:

- [docs/README.md](docs/README.md)
- [docs/OVERVIEW.md](docs/OVERVIEW.md) — quick-read snapshot of coverage and gaps
- [docs/mastery-guide.md](docs/mastery-guide.md) — how to learn interactively with `/pmexpert`
- [docs/getting-started.md](docs/getting-started.md)
- [docs/learning-paths.md](docs/learning-paths.md)
- [docs/rates_credit_mortgages_roadmap.md](docs/rates_credit_mortgages_roadmap.md) — sequenced rates/credit/mortgages path, zero to proficient
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [SDLC.md](SDLC.md)
- [SETUP.md](SETUP.md)
- [ROADMAP.md](ROADMAP.md)

## Recommended workflow

Follow this sequence:

Read → predict → derive → type code yourself → test → compare with reference → explain

That discipline is the project’s core operating model.
