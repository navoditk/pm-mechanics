# Tutor Agents

Tutor agents are an optional learning layer over the repository, not a replacement for the repository.

Run one interactively with `/tutor <topic-or-persona>` (see `.claude/skills/tutor/SKILL.md`
for routing and behavior). Session outcomes are logged to `docs/tutor_sessions/`
and tracked in `docs/mastery.md`.

For a direct analytics answer instead of a teaching session, use
`/pm-query <question>` (`.claude/skills/pm-query/SKILL.md`) — it calls the
actual `src/pm` function and cites it, rather than teaching toward the
answer. See `reference/concepts/agentic_pm_analytics.md` for how the two
skills relate.

To work through the *entire* curriculum rather than one topic at a time,
use `/pmexpert` (`.claude/skills/pmexpert/SKILL.md`) — a single,
self-contained trainer with no second skill to invoke. `/pmexpert` alone
teaches the next weak-or-untested concept in curriculum order;
`/pmexpert quiz` runs 10 rapid multiple-choice questions (`/pmexpert quiz 20`
for a bigger round); `/pmexpert scenario` applies already-confirmed
concepts to a real `use_cases/*` workflow; `/pmexpert exam` runs a
multi-concept oral assessment ladder; `/pmexpert status` gives a one-line
progress readout. It reads the same persona files and grounding
materials `/tutor` uses, so `/tutor` remains available on its own for a
quick one-off session on a single topic outside a mastery pass. See
[docs/mastery-guide.md](../docs/mastery-guide.md) for a plain-language
walkthrough of all five modes.

All tutors should ground themselves in:
- relevant reference pages,
- current notebook,
- tests/examples,
- curated resources.

Initial tutor roles:
- Concept Tutor
- Fixed-Income Tutor
- Portfolio Construction Tutor
- Assessment Tutor

The tutors should adapt depth from diagnostic questions.
