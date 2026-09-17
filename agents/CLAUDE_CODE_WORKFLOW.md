# Claude Code Workflow

Use Claude Code as a deliberate independent reviewer rather than a second continuous implementation agent.

Good moments:
- after completing an optimization module,
- after designing a risk-model abstraction,
- before major architecture changes,
- when a calculation and test both pass but intuition is uncertain.

Suggested prompt:

> Independently review this module as a portfolio analytics reviewer. Do not assume the existing implementation is correct merely because tests pass. Check the financial definition, mathematical formulation, units, numerical stability, edge cases, and whether the API could cause conceptual misuse. Rank findings by severity. Do not edit until I approve.

## Artifact preview (Claude Code only)

Claude Code is the only agent in this repo's rotation with an Artifact
publishing tool, so keeping the read-only Claude Artifact preview
(linked from `README.md`, "Browse without cloning") in sync is a
Claude-Code-specific duty — see `AGENTS.md` rule 17.

After pushing or merging a change to `main` that touches `reference/`,
`curriculum/`, or `use_cases/`:

1. Run `python scripts/build_artifact_preview.py` (rebuilds
   `site_src/_artifact_preview.html`). It imports `markdown`, so the
   `docs` extra must be installed — `pip install -e ".[dev,docs]"`.
2. Publish it with the Artifact tool, passing the **existing** artifact
   URL as `url` so it updates in place rather than creating a new one.
3. Confirm the update landed (spot-check a page that changed) before
   telling the user it's refreshed.

If a Codex or Copilot CLI session made the underlying change, this step
won't have happened yet — it only runs inside a Claude Code session.
Check whether `reference/`, `curriculum/`, or `use_cases/` changed since
the artifact was last published before assuming it's current.
