# Git Workflow Cheat Sheet

## Start a learning unit

```bash
git switch main
git pull --ff-only
git switch -c learn/09-duration-curve-risk
```

## Checkpoint

```bash
git status
git diff
git add <relevant-files>
git commit -m "learn: complete duration hand calculations"
git push -u origin learn/09-duration-curve-risk
```

## Later checkpoint

```bash
pytest
git add src tests
git commit -m "feat: add duration and DV01 calculations"
git push
```

## Open PR

```bash
gh pr create --base main
```

## Inspect

```bash
gh pr diff
gh pr checks
```

## Merge

```bash
gh pr merge --squash --delete-branch
git switch main
git pull --ff-only
```

If the merge touched `reference/`, `curriculum/`, or `use_cases/`, the
Claude Artifact preview linked from `README.md` is now stale — see
`AGENTS.md` rule 17. In a Claude Code session, refresh it
(`scripts/build_artifact_preview.py`, then republish to the existing
URL); in Codex or Copilot CLI, flag it to the developer instead.
