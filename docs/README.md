# Documentation

This folder is the canonical documentation hub for the repository.

## Start here

- [Getting started](./getting-started.md) — install, orient, and begin the first learning unit
- [Overview](./OVERVIEW.md) — a quick-read snapshot of what the repo actually contains, coverage, and gaps
- [Mastery guide](./mastery-guide.md) — learn interactively with `/pmexpert` instead of picking notebooks by hand
- [Learning paths](./learning-paths.md) — choose a route by goal or time horizon
- [Rates, credit, and mortgages: zero to hero](./rates_credit_mortgages_roadmap.md) — a fully sequenced fixed-income path with a reference page, notebook, and verified resources at every step
- [Roadmap](../ROADMAP.md) — long-term curriculum and milestones
- [Architecture](./ARCHITECTURE.md) — repository structure and design intent
- [Workflow](../SDLC.md) — branch, checkpoint, PR, and merge discipline
- [Progress](./PROGRESS.md) — current status, milestones, and module completion

## Repository map

- `curriculum/` — structured learning tracks and bootcamps
- `reference/` — durable PM/FICC concept and instrument reference pages
- `notebooks/` — hands-on learning labs and worked examples
- `src/pm/` — reusable deterministic analytics library
- `tests/` — correctness checks for formulas and implementations
- `use_cases/` — realistic PM workflows built from multiple concepts
- `agents/` — agent operating instructions and workflows
- `tutors/` — tutor prompts and learning support
- `resources/` — curated external references

## Principles

- Read before coding
- Do manual derivations before agent help
- Prefer deterministic formulas over API-driven complexity
- Keep reusable logic in `src/pm/`
- Preserve notebooks as teaching artifacts
- Test the math, then explain it clearly

## Recommended path

1. Read [getting started](./getting-started.md)
2. Choose a learning path in [learning paths](./learning-paths.md)
3. Open the matching notebook
4. Review the concept page in `reference/`
5. Implement and test reusable logic in `src/pm/`
6. Update progress in [PROGRESS](./PROGRESS.md)

Or skip steps 2–4 and let `/pmexpert` pick the next concept for you — see
the [mastery guide](./mastery-guide.md).
