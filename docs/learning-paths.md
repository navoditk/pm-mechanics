# Learning paths

Choose the path that matches your goal.

## Path A — Foundations sprint

Use:

- `curriculum/bootcamp_01_foundations/README.md`

Best for:
- rapid PM foundations
- portfolio optimization basics
- fixed-income vocabulary
- initial FICC fluency

## Path B — FICC deep dive

Recommended after foundations:

1. Fixed-income foundations
2. Rates and curve analysis
3. Credit and default/recovery concepts
4. Securitized products and mortgages
5. FX and commodities
6. Scenario and attribution integration

Key notebooks:

- `notebooks/fixed_income/08_bond_math.ipynb`
- `notebooks/fixed_income/09_duration_curve_risk.ipynb`
- `notebooks/fixed_income/14_curve_construction_forwards.ipynb`
- `notebooks/fixed_income/20_z_spread_and_credit_curves.ipynb`
- `notebooks/fx_commodities/24_fx_and_commodities.ipynb`

For rates, credit, and mortgages specifically, this sketch is the entry
point, not the full route — see [Rates, credit, and mortgages: zero to
hero](./rates_credit_mortgages_roadmap.md) for every step from bond
pricing through TBA/dollar roll and CMO/REMIC structuring, each with a
reference page, notebook, and verified external resources.

## Path B2 — Equity portfolio management

Recommended after foundations, alongside or after Path B:

1. Dividend discount models and relative valuation
2. CAPM, beta, and equity risk premium
3. Equity factor investing and active share
4. Shareholder yield and total shareholder return

Key notebooks:

- `notebooks/equity/28_equity_valuation_and_capm.ipynb`
- `notebooks/equity/29_active_share_factors_and_shareholder_yield.ipynb`

## Path C — Portfolio construction specialist

Focus on:

- portfolio theory
- mean-variance optimization
- risk and covariance models
- constraints and transaction costs
- robust optimization and Bayesian views

Key content:

- `notebooks/optimization/04_efficient_frontier.ipynb`
- `notebooks/optimization/05_constrained_optimization.ipynb`
- `notebooks/optimization/26_shrinkage_and_black_litterman.ipynb`
- `notebooks/optimization/27_risk_parity_and_robust_optimization.ipynb`

## Path D — Quick reference

Start at:

- `reference/index.md`

This is the fastest route when you already know the topic and need the formula, intuition, example, and code recipe.

## Path E — Use-case driven

Start at:

- `use_cases/index.md`

This is the best option when you want to learn by applying PM concepts to real portfolio problems such as hedging, spread shocks, and benchmark-relative analysis.

## Path F — Agentic PM analytics

Start with:

- `reference/concepts/agentic_pm_analytics.md`

This route focuses on the agent layer: tool schemas, grounded answers, evaluations, and deterministic analytics interfaces rather than new financial math.

## Path G — Interactive mastery

Start with:

```
/pmexpert
```

This is the odd one out among the paths above: instead of choosing where
to start, `/pmexpert` chooses for you — it teaches the next concept you
haven't mastered, in curriculum order, one question at a time, and
remembers your progress automatically. Use `/pmexpert quiz` for a fast
multiple-choice check, `/pmexpert scenario` to apply confirmed concepts to
a real use case, or `/pmexpert exam` for a tougher multi-concept checkpoint.

See [docs/mastery-guide.md](./mastery-guide.md) for a full walkthrough.
This is the recommended starting point if you'd rather be guided than
pick a path yourself.
