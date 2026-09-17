# Setup and workflow

This file is a practical workflow guide. The canonical onboarding docs live in [docs/getting-started.md](docs/getting-started.md).

## Recommended flow

Use this repo in a remote-first, branch-based workflow:

**Create remote repo → clone locally → set up environment → branch for the topic → work in notebook + code + tests → push checkpoint → open PR → merge to `main`.**

## Prerequisites

Install:
- Git
- GitHub CLI (`gh`)
- Python 3.12+
- VS Code and/or JupyterLab

Check versions:

```bash
git --version
gh --version
python3 --version
```

Authenticate:

```bash
gh auth login
gh auth status
```

## Step 1 — Create the remote repository

```bash
gh repo create pm-mechanics --private
```

If you prefer a public repo, use `--public` instead.

## Step 2 — Clone locally

```bash
cd ~/GitHub
gh repo clone <YOUR_GITHUB_USERNAME>/pm-mechanics
cd pm-mechanics
```

Check the repo state:

```bash
git remote -v
git status
git branch --show-current
```

## Step 3 — Bootstrap the environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
# add the notebook stack (matplotlib, JupyterLab) when you want to run notebooks:
#   pip install -e ".[dev,notebooks]"
pytest -q
```

Start Jupyter if needed:

```bash
jupyter lab
```

## Step 4 — Start a learning branch

Never do substantial learning work directly on `main`.

```bash
git switch -c learn/01-returns-compounding
```

A good first module is:

```text
curriculum/bootcamp_01_foundations/README.md
notebooks/foundations/01_returns_and_compounding.ipynb
```

## Step 5 — Work in checkpoints

Commit meaningful states, not every keystroke.

### Checkpoint A — manual understanding
After reading, predicting, and doing the hand calculation.

```bash
git add notebooks/foundations/01_returns_and_compounding.ipynb
git commit -m "learn: complete returns and compounding exercises"
git push -u origin learn/01-returns-compounding
```

### Checkpoint B — reusable implementation
After extracting logic into `src/pm/` and adding tests.

```bash
git add src tests
git commit -m "feat: add reusable return calculations"
git push
```

### Checkpoint C — docs and review
After updating the reference and progress docs.

```bash
pytest -q
git add reference docs README.md
git commit -m "docs: complete returns learning module"
git push
```

## Step 6 — Open a pull request

```bash
gh pr create --base main --head learn/01-returns-compounding --title "Learn: returns and compounding"
```

Review the diff and verify the financial logic before merge.

## Step 7 — Merge and continue

Only merge to `main` when:
- the manual exercise is complete,
- tests pass,
- documentation is updated,
- the concept is understandable in plain PM language.

Then:

```bash
gh pr merge --squash --delete-branch
git switch main
git pull --ff-only
```

## Branch naming conventions

Use short, clear names:

```text
learn/<module>
feat/<capability>
fix/<bug>
docs/<topic>
refactor/<area>
chore/<maintenance>
```

## Relationship to docs

- [docs/getting-started.md](docs/getting-started.md) — best place to start
- [docs/learning-paths.md](docs/learning-paths.md) — choose your route
- [docs/PROGRESS.md](docs/PROGRESS.md) — active status and completion tracking
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — repo design and layering

Examples:

```text
learn/09-duration-curve-risk
feat/key-rate-duration
docs/fixed-income-glossary
fix/dv01-frequency-handling
```

## Commit-message conventions

Recommended lightweight Conventional Commit style:

```text
learn: complete duration hand calculations
feat: add key-rate duration approximation
test: cover spread-duration sign convention
docs: add curve-steepener reference page
fix: correct annualization units
refactor: separate rates and credit risk helpers
chore: update development dependencies
```

## Sync discipline

At the start of every session:

```bash
git switch main
git pull --ff-only
git switch <your-working-branch>
git rebase main
```

Before pushing:

```bash
git status
git diff
pytest
git push
```

Avoid `git push --force` unless you understand why it is needed. If you must update a rebased personal branch, prefer:

```bash
git push --force-with-lease
```

## Recommended GitHub settings

Once the repo exists, configure:

- `main` as default branch
- require pull requests before merging
- require status checks when CI is added
- squash merge preferred
- automatically delete head branches after merge
- Issues enabled
- Actions enabled

For a personal learning repository these can start lightweight, then become stricter as collaborators are added.

## Daily end-of-session checklist

```bash
pytest
python scripts/check_repo.py
git status
git log --oneline -5
git push
```

Update:

```text
docs/PROGRESS.md
```

with:
- what you learned,
- what you implemented manually,
- what an agent changed,
- tests run,
- next branch/module.
