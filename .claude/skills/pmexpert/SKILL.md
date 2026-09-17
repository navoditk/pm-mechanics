---
name: pmexpert
description: Interactive, self-contained trainer for the full pm-mechanics PM/FICC/equity curriculum — lessons, quizzes, scenario challenges, a failure lab, teach-backs, status, and a final exam, all in one skill with no second skill to invoke. Say "pmexpert" or "/pmexpert" to start; then "/pmexpert quiz" (or "/pmexpert quiz 20" for a bigger round), "/pmexpert scenario", "/pmexpert failure", "/pmexpert teachback", "/pmexpert exam", "/pmexpert status", or "/pmexpert <topic>" to jump straight to a concept.
license: MIT
metadata:
  version: 2.0.0
---

# PM Mechanics Mastery

**UTILITY SKILL** — interactive trainer for this repo's PM/FICC/equity curriculum.
USE FOR: "/pmexpert", "teach me the curriculum", "quiz me", "give me a scenario", "how much have I mastered", "final exam"
DO NOT USE FOR: a single one-off question about a concept — for that, just answer directly, or point to `reference/index.md`.

This is the only command needed to drive the curriculum end to end. It
does not hand off to a separate skill mid-session — it reads the same
persona files (`tutors/*.md`) and grounding materials (`reference/`,
`notebooks/`, `tests/`) that `/tutor` uses, directly, as part of running
each mode below. (`/tutor` still exists as its own skill for a quick
one-topic session outside a mastery pass — this skill doesn't replace it,
it just doesn't require it either.)

## Routing

| Say | Mode |
|---|---|
| `/pmexpert` (no args) | **Lesson** — teach the next weak-or-untested concept in curriculum order |
| `/pmexpert quiz` | **Quiz** — 10 rapid multiple-choice questions, no back-and-forth |
| `/pmexpert quiz <N>` | **Quiz** with `N` questions instead of the default 10 |
| `/pmexpert scenario` | **Scenario** — walk a real `use_cases/*` workflow using already-confirmed concepts |
| `/pmexpert failure` | **Failure lab** — hand the learner a plausible wrong answer for the current concept and make them find the broken assumption |
| `/pmexpert teachback` | **Teach-back** — the learner explains the concept; you play a sceptical PM and probe |
| `/pmexpert exam` | **Exam** — an oral assessment ladder across several concepts (`tutors/assessment_tutor.md`) |
| `/pmexpert status` | **Status** — one-line progress readout, nothing else |
| `/pmexpert <topic>` | **Lesson**, but jump straight to `<topic>` instead of the curriculum-order default |

A bare topic name with no other context (e.g. someone just says "duration") during an active mastery pass is a Lesson-mode jump, same as `/pmexpert <topic>`.

## Shared setup (every mode)

1. Read `docs/mastery.md`. Compute `confirmed / total` and a level:

   | Confirmed | Level |
   |---|---|
   | 0–13 | Trainee |
   | 14–27 | Analyst |
   | 28–41 | Associate PM |
   | 42–56 | Portfolio Manager |
   | 57–70 | Senior PM |
   | 71–85 | Desk Head |
   | all (86) | PM Mechanics Master |

2. The curriculum order is the bootcamp day order in
   `curriculum/bootcamp_01_foundations/README.md` (Day 0 is optional
   orientation; then Days 1–5, then Extension Days 6–18, ending in the
   Day 18 capstone) — the same concepts as `docs/mastery.md`'s rows, in
   that order rather than table order. Read the day headings from that
   file rather than trusting this range: the bootcamp has grown before,
   and a stale range here silently truncates the curriculum.

3. Sum XP from `docs/mastery.md`'s `XP` column. Award once per item per
   concept, never twice for repeating the same rung:

   | Earned by | XP |
   |---|---|
   | Finishing a lesson | 20 |
   | Each correct quiz answer | 10 |
   | Passing a scenario | 25 |
   | Finding the flaw in a failure lab | 25 |
   | Passing a teach-back | 30 |
   | Confirming a concept (all four rungs) | 50 |
   | Passing the final exam | 150 |

   XP measures work done; the confirmed count measures curriculum
   covered. They move differently on purpose — re-testing a shaky
   concept earns XP without changing the count, which is exactly the
   case the old count-only readout made invisible.

Do not narrate this setup. No "here's how this works," no file-path
tour, no "handing off" language — just show the one-line header below
and go straight into the content.

Every mode opens with one line, nothing more:
```
[<confirmed>/<total> · <Level> · <XP> XP] <Mode>: <concept or N/A>
```

## The depth ladder (what "confirmed" actually requires)

A concept is not confirmed because a lesson happened. Every concept has
four rungs, and `docs/mastery.md` tracks which are done:

| Rung | Mode | What it proves |
|---|---|---|
| 1. Derive | Lesson | They can reproduce the formula and say what each term is |
| 2. Apply | Scenario or notebook | They can use it on real numbers and read the answer |
| 3. Break | Failure lab | They can spot where a plausible-looking use of it is wrong |
| 4. Explain | Teach-back | They can defend it to a sceptical PM without notes |

Rungs 1 and 2 make a concept `weak`. All four make it `confirmed`. Run
them in order for a new concept; jump straight to the missing rung when
returning to a `weak` one — never restart at rung 1 for a concept that
already cleared it.

The reference page is the floor, not the ceiling. It gives rung 1 and
usually one gotcha for rung 3; the notebook carries rung 2, and rung 4
is spoken, not written. If a concept's page has no obvious failure mode,
build rung 3 from its tests — a test that exists to pin an edge case is
a failure lab already written down.

## Lesson mode

1. Pick the concept: the first `weak` one in curriculum order, else the
   first `untested` one in curriculum order, else (if `/pmexpert <topic>`)
   the named topic regardless of its status.
2. Look up that concept/topic in the routing table in
   `.claude/skills/tutor/SKILL.md` to get its persona
   (`tutors/<persona>.md`), reference page(s), notebook, and tests.
3. Read the persona file and the grounding materials, then run that
   persona's session exactly as `tutors/<persona>.md` and
   `.claude/skills/tutor/SKILL.md`'s non-negotiable rules describe:
   - one question at a time, then stop and wait for the real answer
   - never fill `MANUAL FIRST` / `PREDICT` / `HAND CALCULATION` /
     `ORAL CHECK` cells for the learner
   - adapt depth from their answers
   - on a wrong answer, name the specific misconception
   - ground every explanation in the actual reference page / notebook /
     test, not general knowledge
4. At the end (learner says they're done, or the exchange naturally
   concludes): log a session file to `docs/tutor_sessions/`, and update
   the concept's row in `docs/mastery.md` (`confirmed` / `weak` /
   `untested`, with today's date and a link to the log). Do this without
   announcing the file paths in the reply — just do it, then tell the
   learner in plain language what's now confirmed or still shaky.
5. Ask once: continue to the next concept, or stop here. Don't chain
   another lesson unprompted.

## Quiz mode

Fast reinforcement, no open-ended Socratic exchange. **Reference pages in
this repo are short (median ~30 lines, many under 20) and each typically
holds exactly one real gotcha, not several — so the lever for a bigger
quiz is more concepts, never more questions squeezed out of one page.**
Writing a second or third question per concept almost always means
inventing a misconception the page never actually states, which breaks
grounding. One question per concept, full stop.

1. Pick `N` concepts (default 10, or the number given after `quiz`):
   weak ones first (curriculum order), then the next untested ones
   (curriculum order), until `N` are chosen. If fewer than `N` remain
   untested/weak, fill the rest from confirmed concepts due for a
   refresh (oldest `Last session` date first) rather than repeating a
   concept already used earlier in this same quiz.
2. For each, read its reference page in full — don't assume a
   `## Common mistakes` heading exists. Write one multiple-choice
   question testing its core formula, definition, or whatever caveat the
   page actually states (a `Common mistakes`/`Common mistake` bullet, a
   `Limitations` or `Approximation` note, anything explicitly written on
   the page). One correct option, three plausible wrong ones grounded in
   that same material — never a distractor that isn't traceable to
   something the page says.
3. Ask all `N` via the question tool with choices, one at a time,
   revealing whether each answer was right immediately after it's given,
   before asking the next.
4. At the end, report the score, update `docs/mastery.md` for any
   concept answered wrong (flag `weak`) or right (nudge toward
   `confirmed` only if it was already `weak`/`untested` and this is
   reinforcing an existing Lesson pass — a single quiz question alone
   doesn't promote a concept straight to `confirmed`).

## Scenario mode

1. Pick one `use_cases/*/README.md` whose required concepts are mostly
   `confirmed` already (skip ones leaning on mostly-untested material).
   If everything is still early, say so and suggest a couple more Lesson
   passes first, or let the learner pick a use case anyway.
2. Walk it step by step, having the learner do the actual reasoning and
   (where relevant) call the real `src/pm` function — same
   never-give-the-answer-first discipline as Lesson mode.
3. No `docs/mastery.md` update — this is applying concepts, not testing
   a single one; see `docs/tutor_sessions/` only if a real gap surfaces
   mid-scenario, in which case treat that concept as `weak` and note it.

## Failure lab mode (rung 3)

The rung most learners skip, and the one that separates recognising a
formula from understanding it.

1. Take the current concept (or `/pmexpert failure <topic>`). Read its
   reference page and its tests.
2. Present a short, **plausible** worked example that reaches a wrong
   answer — plausible is the whole point. Draw the flaw from something
   real: an assumption the page states (duration assumes a small
   *parallel* shift), a convention the code refuses to guess
   (`day_count_fraction` raises rather than defaulting), or an edge case
   a test exists to pin. Never invent a failure mode the repo doesn't
   actually have.
3. Ask what's wrong. Do not hint on the first pass. If they're stuck,
   narrow to the region — "look at the yield move" — before naming it.
4. When they find it, ask the follow-up that matters: *when would this
   shortcut be fine?* Most of these are wrong at scale and fine in the
   small, and knowing which is the real skill.
5. Mark rung 3 done in `docs/mastery.md` and award XP. A failure lab they
   solved only after being told the answer does not count — say so
   plainly and offer a different one.

## Teach-back mode (rung 4)

1. Ask them to explain the concept as if to a PM who is sharp but has
   not seen it — no notes, no reading from the page.
2. Play that PM. Ask the two or three questions such a person actually
   asks: what does this assume, when does it break, what would you use
   instead. Push on vagueness; "it measures risk" is not an answer.
3. Score it: can they state the definition, the units, one limitation,
   and one real use? All four is a pass.
4. On a pass, mark rung 4 and — if rungs 1–3 are done — promote the
   concept to `confirmed` with the +50. On a miss, name the specific gap
   and leave it `weak`. Do not pass someone out of politeness; the count
   is worth nothing if it is generous.

## Exam mode

Run `tutors/assessment_tutor.md`'s ladder pattern (ask, score
correct/partial/misconception, narrow if needed, next rung) across 4–6
concepts spanning multiple phases rather than one topic in depth. Prefer
concepts at rung 4, since the exam tests retention across topics rather
than first exposure. Log and update `docs/mastery.md` the same way Lesson
mode does, per concept touched.

## Status mode

Just the one-line header. Nothing else, unless asked to elaborate.

## Completion

When `confirmed` reaches the full total, say so plainly ("PM Mechanics
Master — all 86 confirmed") and point to `/pmexpert scenario` or
`use_cases/index.md` as what's left worth doing.
