# Learning This Repo with /pmexpert

Everything else in this repo assumes you're working through notebooks and
reference pages by hand. `/pmexpert` is the interactive alternative: one
command that teaches the curriculum to you, one question at a time,
adapting to your answers, and remembering exactly where you left off. You
don't need to track progress yourself or know which notebook comes next —
just type it and go.

## Start here

Type:

```
/pmexpert
```

That's it. It reads your current progress, tells you where you are in one
line, and asks the next question.

## The seven ways to use it

| Command | What it does | When to use it |
|---|---|---|
| `/pmexpert` | **Lesson** — teaches the next concept you haven't mastered yet, one question at a time, adapting depth to your answers | Default. Use this most of the time — it's the one that actually builds understanding |
| `/pmexpert quiz` | 10 rapid multiple-choice questions across different concepts, right/wrong revealed immediately | A fast gut-check across many topics, or a warm-up before a lesson |
| `/pmexpert quiz 20` | Same, a bigger round | When you have more time and want broader coverage |
| `/pmexpert scenario` | Applies concepts you've already confirmed to a real portfolio workflow | Once you've got some concepts confirmed and want to see them used together, not just recited |
| `/pmexpert failure` | Hands you a plausible-looking worked example that reaches a **wrong** answer, and asks you to find the flaw | The rung most people skip. Recognising a formula and spotting its misuse are different skills |
| `/pmexpert teachback` | You explain the concept; it plays a sceptical PM and probes what you assumed, when it breaks, what you'd use instead | Last step before a concept counts as confirmed — if you can't defend it cold, you don't have it yet |
| `/pmexpert exam` | A tougher, ladder-style oral check across several concepts at once, narrowing in on weak spots | As a checkpoint after finishing a phase (e.g. all of fixed income) |
| `/pmexpert status` | Just reports how far along you are — nothing else | Any time you want a quick read without starting a session |
| `/pmexpert <topic>` (e.g. `/pmexpert duration`) | Jumps straight to a specific concept instead of the default order | When you already know what you want to work on |

## What a lesson actually looks like

```
[1/55 · Trainee] Lesson: Returns and compounding

A stock is worth $100. It rises 50%, then falls 50%. Cumulative return —
0%, above 0%, or below 0%? What's the ending dollar value?
```

You answer in your own words — there's no menu to pick from, just reply
normally. If you're right, it moves forward with a worked example; if
you're off, it names exactly what you got wrong instead of just saying
"not quite" and giving the answer away. It never fills in the answer for
you, even if you're stuck — it'll narrow the question or give a hint
instead.

## A realistic first session

1. Type `/pmexpert`. Say it shows `1/55 · Trainee` with duration already
   confirmed from an earlier session — first stop is Day 1, Returns and
   compounding.
2. Answer honestly. Right or wrong, the process is the same either way —
   you'll get an explanation and a worked example regardless.
3. Once you've got it, it asks whether to keep going or stop here.
4. Come back anytime — tomorrow, next week — and type `/pmexpert` again.
   It resumes exactly where you left off. No separate command, no notes
   to keep yourself.

## What "confirmed" means — the four rungs

A concept isn't confirmed because you sat through a lesson. Each one has
four rungs, and you clear them with different modes:

| Rung | Cleared by | What it proves |
|---|---|---|
| **D**erive | `/pmexpert` | You can reproduce the formula and say what each term is |
| **A**pply | `/pmexpert scenario`, or a notebook | You can use it on real numbers and read the answer |
| **B**reak | `/pmexpert failure` | You can spot where a plausible-looking use of it is wrong |
| **E**xplain | `/pmexpert teachback` | You can defend it to a sceptical PM without notes |

Any rung cleared makes a concept *weak*; all four make it *confirmed*.
You don't restart — returning to a half-done concept picks up at the
missing rung.

The deliberate part is that rung 3 is hard to fake. The failure labs are
built from things this repo actually states — an assumption on the
reference page, a convention the code refuses to guess, an edge case a
test exists to pin — never an invented mistake. And a lab you only
solved after being told the answer doesn't count.

## How it remembers your progress

Your status lives in `docs/mastery.md`, updated automatically at the end
of every session. Each concept shows its rungs as four characters —
`····` untouched, `DA··` derived and applied, `DABE` complete — plus an
XP total. You never need to touch that file yourself, but it's plain
markdown, and its header explains the notation.

XP and the confirmed count move differently on purpose. XP measures work
done; the count measures curriculum covered. Re-testing a shaky concept
earns XP without changing the count, which is exactly the progress the
old count-only readout made invisible.

## A few tips

- **Answer for real.** Guessing to get past a question defeats the
  point — the whole repo is built around deriving things yourself, not
  recognizing the right answer when it's shown to you.
- **It's fine to stop mid-lesson.** No penalty, no timer.
- **Mix modes.** Lessons build understanding, quizzes are a fast check,
  scenarios show concepts working together, exams are the toughest
  self-check. None of them replaces the others.
- Once every concept is confirmed, `/pmexpert` will say so and point you
  at `use_cases/` — applying what you know instead of studying more.

## How this relates to /tutor and /pm-query

`/pmexpert` is the recommended default — it's the only command most
learners need for the whole curriculum. Two narrower tools exist
alongside it:

- **`/tutor <topic>`** — the same kind of teaching session, but for
  exactly one topic, with no curriculum sequencing or progress tracking.
  `/pmexpert` actually uses this same logic under the hood.
- **`/pm-query <question>`** — not a teaching tool at all. Give it a
  specific question (e.g. "what's the DV01 of a 5Y 5% bond at 4%
  yield?") and it runs the real code and gives you the number, cited.
