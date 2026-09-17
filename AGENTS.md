# Agent Instructions for This Repository

This is a learning-first financial analytics repository.

## Hard rules

1. Never fill `MANUAL FIRST`, `PREDICT`, `HAND CALCULATION`, or `ORAL CHECK` sections unless the user explicitly says they completed or want the answer.
2. Financial logic must have:
   - a documented definition,
   - clear units,
   - a worked deterministic example,
   - tests.
3. Preserve notebooks as teaching artifacts.
4. Reusable code belongs in `src/pm/`.
5. Do not add market-data/API complexity before the deterministic calculation works.
6. Prefer small transparent functions over opaque frameworks.
7. State approximation limitations for risk sensitivities.

## Auditing rules

8. **Enumerate the repo's convention before writing a detector for it.**
   Never grep for the pattern you assume a repo uses — list what it
   actually uses first, then match that. This has produced three wrong
   answers in this repo already:

   - Searching for `## Common mistakes` missed `## Common mistake`
     (singular), `## Limitations`, `## Important limitation`, and
     `## Approximation`, and reported 25 missing failure-mode sections
     when the real number was 9.
   - Searching quiz *question text* for `src/` missed that the real
     signal is the `citation` field, and wrongly condemned a well-formed
     quiz bank as half-misaligned.
   - A blind `/master` → `/pmexpert` replace rewrote every `mastery.md`
     path to `pmexperty.md`, because the old token is a substring of a
     real filename.

   The cheap habit that prevents all three:

   ```bash
   grep -rhE "^## " reference/ | sort | uniq -c | sort -rn   # what headings exist?
   grep -rn "<old-token>" . | grep -v "<expected-context>"   # what else matches?
   ```

9. **After a repo-wide replace, grep for the corrupted token, not just
   the new one.** `grep -rn "pmexperty"` found the damage instantly;
   `grep -rn "/pmexpert"` looked clean and would have shipped it. A
   token that is a substring of a filename, heading, or identifier will
   corrupt silently and no test will catch it, because the damage is in
   prose and paths.

10. **A count in a doc is a claim; verify it against the tree.** Counts
    in `docs/OVERVIEW.md` and skill level ladders drift whenever content
    is added. Measure, then edit — and when a count changes, check
    whether a skill's thresholds depend on it.

## Git / SDLC rules

11. Before making repo-wide edits, inspect `git status` and the current branch.
12. Do not make learning-feature changes directly on `main`.
13. Keep changes scoped to the current issue/module.
14. Run relevant tests before proposing a commit.
15. Update `docs/PROGRESS.md` at module completion.
16. Never commit secrets, credentials, tokens, generated virtual environments, or local `.env` files.
17. After pushing or merging to `main` a change that touches `reference/`,
    `curriculum/`, or `use_cases/` (the content the Claude Artifact
    preview embeds), refresh and republish it: run
    `scripts/build_artifact_preview.py`, then republish to the *same*
    URL already linked from `README.md` — never a new one. This needs
    the Claude Code Artifact tool. If you're working via Codex or
    Copilot CLI, you don't have that tool — say so explicitly and tell
    the developer to ask Claude Code to publish the refresh, rather than
    silently skipping it. See `agents/CLAUDE_CODE_WORKFLOW.md`,
    `agents/CODEX_WORKFLOW.md`, `agents/COPILOT_WORKFLOW.md`.
