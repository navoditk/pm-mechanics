# GitHub Copilot Workflow

Use Copilot mainly as an editor and GitHub workflow accelerator.

Good uses:
- small boilerplate,
- docstrings,
- type hints,
- simple test parameterization,
- routine Git/GitHub actions,
- code navigation.

Avoid allowing inline completion to write:
- the first version of a formula you are trying to learn,
- an optimization objective before you formulate it,
- bond-duration calculations before hand derivation.

Copilot CLI can also be useful for plan/review/GitHub integration once a learning task is already understood.

## Artifact preview — flag, don't skip

If a push or merge touched `reference/`, `curriculum/`, or `use_cases/`,
the read-only Claude Artifact preview linked from `README.md` is now
stale (see `AGENTS.md` rule 17). Copilot has no Artifact publishing
tool, so it can't refresh it directly — say so explicitly and tell the
developer to ask Claude Code to run `scripts/build_artifact_preview.py`
and republish it, rather than leaving the staleness unmentioned.

## The learning skills are available here

They are not Claude Code-only. `.github/skills/` carries Copilot discovery loaders for
all three, each pointing at the canonical package under `skills/`:

- `pmexpert` — the guided mastery path, one rung at a time
- `tutor` — a per-topic tutor persona
- `pm-query` — ask the analytics library a question in plain English

Say the skill's name to start. The canonical content is in
`skills/<name>/SKILL.md`; do not edit the loader.

For navigating without a skill, `pm-mechanics topics`, `pm-mechanics
reference <page>` and `pm-mechanics progress` are read-only and need no model.
