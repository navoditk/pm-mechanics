@AGENTS.md

## Why this file exists

`AGENTS.md` is the canonical instruction file for every coding agent used
here — Claude Code, GitHub Copilot, and OpenAI Codex all read it, and it is
the only place the repository's rules are maintained. This file exists solely
to import it.

Claude Code reads `AGENTS.md` directly in most sessions, but falls back to
reading `CLAUDE.md` alone when the session runs on Amazon Bedrock or another
third-party provider, when telemetry is disabled, when `disableAllHooks` or
`allowManagedHooksOnly` is set, on versions before v2.1.277, and on the first
session after an upgrade. Several of those are routine in a corporate
environment.

That matters more here than it looks. Hard rule 1 — never fill in a
`MANUAL FIRST`, `PREDICT`, `HAND CALCULATION`, or `ORAL CHECK` section unless
the learner says they have finished it — guards 276 markers across this
repository, and an agent that has not read it will helpfully supply the
answers and destroy the exercise. Without this import, that rule would be
silently absent in exactly the sessions least likely to notice.

An import rather than a symlink is deliberate: the Edit and Write tools
refuse to write through a symlink, and Git checks a committed symlink out as
a plain text file on Windows clones unless `core.symlinks` is set, leaving
that clone with a one-line `CLAUDE.md` instead of the instructions.

Keep this file a pointer. Anything that applies to every agent belongs in
`AGENTS.md`.
