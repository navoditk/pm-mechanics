# Codex Workflow

Use Codex as the primary repo-aware build agent.

## Start-of-session prompt

Paste this from the repository root:

> Read README.md, ROADMAP.md, LEARNING_PATHS.md, AGENTS.md, resources/README.md, and the README for the curriculum module I am working on. This is a learning-first PM/FICC repository. Do not solve cells or exercises marked MANUAL FIRST, PREDICT, HAND CALCULATION, or ORAL CHECK. Wait for my attempted implementation. When I tell you I have completed one, first review mathematical correctness, dimensions/units, edge cases, and financial interpretation. Explain errors before editing. Then make the smallest necessary correction, extract reusable code into src/pm where appropriate, add or update tests, and update the relevant reference page. Run tests before concluding. Do not silently expand scope.

## During a notebook lab

You:
1. watch/read,
2. derive,
3. type implementation,
4. run it.

Then ask Codex:

> Review the implementation in notebook XX and compare it with the formula in reference/... . Do not rewrite yet. Identify mathematical, numerical, dimensional, and interpretation issues.

After review:

> Apply the agreed correction. Extract the reusable implementation into src/pm/... . Keep the notebook pedagogical. Add tests for hand-calculated examples and invariants.

## End-of-session prompt

> Run relevant tests. Update docs/PROGRESS.md with what was completed, what concepts I demonstrated manually, known limitations, and the exact next notebook/reference page to open. Do not mark a concept complete unless its tests pass and a reference page exists.

## Artifact preview — flag, don't skip

If this session pushed or merged a change touching `reference/`,
`curriculum/`, or `use_cases/`, the read-only Claude Artifact preview
linked from `README.md` is now stale (see `AGENTS.md` rule 17). Codex
has no Artifact publishing tool, so it can't refresh it directly — say
so explicitly at the end of the session and tell the developer to ask
Claude Code to run `scripts/build_artifact_preview.py` and republish it,
rather than leaving the staleness unmentioned.

## The learning skills are available here

They are not Claude Code-only. `.agents/skills/` carries Codex discovery loaders for
all three, each pointing at the canonical package under `skills/`:

- `pmexpert` — the guided mastery path, one rung at a time
- `tutor` — a per-topic tutor persona
- `pm-query` — ask the analytics library a question in plain English

Say the skill's name to start. The canonical content is in
`skills/<name>/SKILL.md`; do not edit the loader.

For navigating without a skill, `pm-mechanics topics`, `pm-mechanics
reference <page>` and `pm-mechanics progress` are read-only and need no model.
