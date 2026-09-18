# Tutor session — 2026-09-17

**Persona:** `tutors/failure_lab_tutor.md`
**Mode:** `/pmexpert failure` (rung 3 — Break)
**Topic:** duration, DV01, convexity, KRD

## Starting state correction

The row was `confirmed` with `····` rungs — a contradiction the ladder
forbids, left over from before rungs existed. The 2026-09-02 session
genuinely cleared Derive (modified duration and DV01, including a
self-caught basis-point slip) and Apply (a +50bp shock, DV01 at price 98,
and a bullet-vs-barbell KRD scenario). Migrated to `weak` / `DA··` / 45 XP.
The old `confirmed` meant only that a lesson had happened.

## Lab presented

A colleague's note sizing downside on a 10Y 4% semi-annual bond at par:
modified duration 8.18, a +300bp selloff, `−8.18 × 0.0300 = −24.53%`,
therefore a mark of 75.47 and a stop-loss at 75.50. Every figure in the
note is arithmetically correct; the flaw is entirely in the unstated
assumption.

Grounded in `reference/fixed_income/duration.md`'s first Common mistakes
bullet ("using it for a large yield move"). Figures verified against
`bond_price`, `modified_duration` and `convexity` before presenting:

| Shock | Duration-only | Actual reprice | Gap |
|---|---|---|---|
| +50bp | −4.09% | −3.99% | 0.10 pts |
| +300bp | −24.53% | −21.32% | 3.21 pts |

## Outcome

Not cleared. The learner did not attempt a diagnosis and ended the session
to return to repository work. One narrowing hint was given ("look at the
size of the yield move") per the persona; the flaw was never named.

**Rung 3 not awarded.** No XP. Duration stands at `DA··` / 45 XP / `weak`,
which is the honest record.

## Gap surfaced (repo, not learner)

`docs/mastery.md` can hold a row whose `Status` contradicts its `Rungs` —
exactly the state duration was in — and nothing checks for it. The skill
says status must follow from the rungs, but that rule had no enforcement.
Addressed outside this session.

## Suggested next action

Re-run `/pmexpert failure duration` with a fresh lab when there is time to
engage with it. The presented lab is now spent for assessment purposes,
since the narrowing hint materially reduced it.
