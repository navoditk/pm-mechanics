# Risk Contribution

## Definitions
Marginal risk contribution:
`MCR_i = (Sigma w)_i / sigma_p`

Component risk contribution:
`CR_i = w_i * MCR_i`

## Identity
`sum_i CR_i = sigma_p`

## Why PMs care
Capital weights and risk weights can be radically different.

## PM question
Which positions are actually driving portfolio volatility?

## Common mistakes
- Reading `CR_i` as "the volatility this position would have on its own."
  It is the position's share of *portfolio* volatility given everything
  else held — remove the position and the remaining contributions all
  change.
- Expecting the components to sum to portfolio *variance*. The identity
  is `sum_i CR_i = sigma_p`, the volatility, not `sigma_p^2`.
- Assuming a contribution cannot be negative. A position that hedges the
  rest of the book has a negative marginal contribution, and that is the
  correct answer, not a sign error.
- Confusing this with contribution to *tracking* error. Same algebra,
  different input: MCTE uses active weights against a benchmark. See
  [MCTE and group risk decomposition](mcte_and_group_risk.md).

## Related
- [Portfolio volatility](portfolio_volatility.md)
- [Factor risk contribution](factor_risk_contribution.md)
- [MCTE and group risk decomposition](mcte_and_group_risk.md)
