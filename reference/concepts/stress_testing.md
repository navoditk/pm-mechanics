# Stress Testing

## One-line definition
Asking "what would happen to the portfolio under this specific, named
shock?" — as distinct from VaR/ES, which ask "what's the loss at a given
statistical confidence level?"

## Why PMs care
VaR/ES are calibrated to historical volatility and assume a return
distribution; they systematically understate tail events that haven't
happened recently (or ever, in this exact form). Stress tests let a PM
reason about specific, plausible-but-rare scenarios directly, independent
of any distributional assumption.

## Two kinds
- **Historical**: replay a real past event (e.g. 2008, the 2013 taper
  tantrum) against today's portfolio.
- **Hypothetical**: construct a scenario by hand (e.g. "2s10s steepens 50bp
  and IG spreads widen 75bp") — this is what `Scenario` in
  `src/pm/scenarios.py` represents.

## Implementation
This repo keeps shocks explicit and separate rather than one aggregator
function — curve, IG spread, HY spread, and equity contributions are
computed individually, then summed, so each is auditable on its own. See
`notebooks/integration/11_scenarios.ipynb` and reuse
`key_rate_return_approximation` (curve), `spread_pnl` (credit), and simple
multiplication (equity) per leg.

## Common mistakes
- picking only scenarios the portfolio is known to survive
- forgetting shocks can partially offset (e.g. falling rates cushioning
  widening credit spreads in a risk-off scenario)

## Related
- [Value at risk](value_at_risk.md)
- [Key-rate duration](../fixed_income/key_rate_duration.md)
- [Backtesting biases](backtesting_biases.md)
