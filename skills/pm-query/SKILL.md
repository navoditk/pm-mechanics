---
name: pm-query
description: Answers a direct PM/FICC analytics question by calling the actual deterministic src/pm function(s) that compute it, never by estimating or reasoning out the number. Use for "/pm-query <question>", e.g. "what's the DV01 of a 5Y 5% bond at 4% yield?"
---

# PM Query (Agentic Analytics Layer)

This skill is the "natural-language query layer" over `src/pm` referenced
in `ROADMAP.md` Phase 12. It is deliberately **not** a tutor — `/tutor`
teaches via Socratic questions and never gives the answer; `/pm-query`
gives a direct answer, but only by running real code.

## Non-negotiable rule

**Never compute or estimate the numeric answer yourself.** Per
`docs/ARCHITECTURE.md`: "The repository should never depend on an LLM for
deterministic financial arithmetic." Every answer must come from actually
executing a function in `src/pm` (e.g. via `python -c "..."` or a short
scratch script), not from reasoning through the formula in your head. If
you catch yourself about to state a number without having run code that
produced it, stop and run the code first.

## Step 1 — find the right tool

Read `docs/tool_schema.json` (regenerate with
`python scripts/generate_tool_schema.py > docs/tool_schema.json` if it
looks stale — `tests/test_tool_schema.py` checks this in CI) to find
candidate function(s): name, module, parameters, and (where present) a
docstring. Cross-reference `reference/index.md` and the `/tutor` skill's
routing table (`skills/tutor/SKILL.md`) for the matching concept
page, which usually names the exact function too.

If no function matches the question, say so plainly and point to the
closest conceptual reference page (many advanced topics — OAS, credit
migration, hierarchical risk parity, multi-period optimization — are
intentionally conceptual-only; check for a "why this isn't implemented"
section before assuming it's just missing).

## Step 2 — get real inputs

Identify every argument the function needs. If the question doesn't
specify one (e.g. asks for "DV01" without a coupon or maturity), ask the
user rather than inventing a plausible-sounding number — a fabricated
input produces a real-looking but meaningless output.

## Step 3 — run it

Execute the function for real, e.g.:
```bash
.venv/bin/python -c "from pm.fixed_income.duration import dv01; print(dv01(0.04, face=100, coupon_rate=0.05, years=5, frequency=2))"
```
Use the project's `.venv` (or whatever environment has the package
installed) so the exact code in `src/pm` runs, not a re-derivation of it.

## Step 4 — answer with explanation (grounding + explainability)

State the number, then explicitly cite:
- the exact function and module called (`pm.fixed_income.duration.dv01`)
- the inputs passed
- the matching reference page, if one exists, for the underlying concept
  and its stated limitations (e.g. an approximation caveat)

A bare number with no citation is not an acceptable answer from this
skill.

## Step 5 — log the query (observability)

Append a new file to `docs/analytics_queries/<YYYY-MM-DD>-<slug>.md`:
the question asked, the function(s) called with their inputs, the result,
and the reference page cited. One file per query, never edited after
creation — mirrors `docs/tutor_sessions/`.

## Evals

There is no automated eval harness for this skill's routing behavior
(that would need a live agent harness this repo doesn't have) - instead,
`docs/agentic_analytics_evals.md` is a manually-run checklist of example
queries with their expected function/output, kept honest rather than
faking automation that doesn't exist.
