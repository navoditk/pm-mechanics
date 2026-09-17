# Getting started

## Two ways to learn this repo

**Manual** — work through curated readings, notebooks, and reference
pages yourself, at whatever pace and depth you choose. The rest of this
page describes that path.

**Interactive** — type `/pmexpert` and let it teach the curriculum to you,
one question at a time, tracking progress automatically. See the
[mastery guide](./mastery-guide.md) for how it works. This is the faster
way to get started if you don't want to pick notebooks and track
completion by hand.

Both use the same underlying material (reference pages, notebooks,
tests) — pick whichever fits how you like to learn, or mix the two.

## Recommended first session (manual path)

Use this sequence:

1. Read this page
2. Review the repo overview in the root [README.md](../README.md)
3. Set up the GitHub workflow in [SETUP.md](../SETUP.md)
4. Run the test suite
5. Open the first foundations notebook and complete the first manual exercise

## Setup

Create a virtual environment, install dependencies, and confirm the repo is healthy:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
# add the notebook stack (matplotlib, JupyterLab) when you want to run notebooks:
#   pip install -e ".[dev,notebooks]"
pytest -q
```

## Starting from zero

If you haven't taken a portfolio-theory or linear-algebra course before,
start with `notebooks/foundations/00_orientation.ipynb` first — it
confirms your environment actually works, explains the PREDICT/MANUAL
FIRST/ORAL CHECK cycle every later notebook uses, and walks through the
one piece of matrix math (`w' Sigma w`) the rest of the curriculum
assumes. Keep [reference/glossary.md](../reference/glossary.md) open
alongside any notebook as a fast look-up for unfamiliar terms.

## The intended experience

A concept such as covariance should be encountered in this order:

1. Curated reading and concept review
2. A prediction question
3. A small hand calculation
4. A notebook with an empty implementation cell
5. A code recipe you type yourself
6. Experiments that change assumptions
7. Extraction into `src/pm/`
8. Unit tests
9. A concise PM explanation
10. Optional deep-dive tutor support

## Do not start by asking an agent to build the repo

The repo already contains the structure. Coding agents are most useful after you have attempted the financial logic yourself.

## Version-control workflow

Before starting a learning unit, read:

- [SETUP.md](../SETUP.md)
- [SDLC.md](../SDLC.md)
- [docs/ARCHITECTURE.md](./ARCHITECTURE.md)

Work on short-lived branches, push checkpoints, and merge via pull request only after tests and documentation are in order.

## First milestone

The default first module is:

- `curriculum/bootcamp_01_foundations/README.md`
- `notebooks/foundations/01_returns_and_compounding.ipynb`

This is the ideal place to begin if you want a structured introduction to returns, diversification, risk, and portfolio basics. If you're starting from zero, do `00_orientation.ipynb` first — see "Starting from zero" above.
