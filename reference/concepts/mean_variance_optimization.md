# Mean–Variance Optimization

## Core problem
The utility formulation this repo's `mean_variance` uses:

`maximize mu^T w - (lambda / 2) * w^T Sigma w`

subject to portfolio constraints.

## Objects
- `mu`: expected return vector
- `Sigma`: covariance matrix
- `w`: weights
- `lambda`: risk-aversion coefficient

## Why the 1/2 matters
This objective's first-order condition is `mu = lambda * Sigma @ w` —
exactly what [`market_implied_returns`](black_litterman.md) inverts to
recover a market-implied prior from observed weights. Drop the 1/2 and
that round trip (reverse-optimize market weights into a prior, then feed
the prior back into the optimizer) no longer returns the market weights
at the same `lambda` — it only closes at `lambda / 2`. See
`tests/test_robust.py::test_market_implied_returns_round_trips_through_mean_variance`.

## Why PMs care
It formalizes the tradeoff between expected return, risk, and implementation constraints.

## Important limitation
Optimal weights can be extremely sensitive to estimation error, especially in expected returns.

## Common mistakes
- Trusting the weights more than the inputs. The optimiser is exact; the
  expected returns are not. Small changes in `mu` move the solution a
  long way, which is the limitation stated above and the reason
  [covariance shrinkage](covariance_shrinkage.md) and
  [Black-Litterman](black_litterman.md) exist.
- Dropping the `1/2` from the objective and still expecting the
  Black-Litterman round trip to close. It only closes at `lambda / 2` —
  pinned by
  `tests/test_robust.py::test_market_implied_returns_round_trips_through_mean_variance`.
- Comparing `lambda` across problems with different return units. Risk
  aversion is only meaningful relative to the scale of `mu` and `Sigma`.
- Treating an infeasible problem as a solver failure. This repo's
  optimizers raise rather than returning `None` or silently relaxing a
  constraint — an infeasible set of constraints is an answer about the
  constraints.

## Related
- [Efficient frontier and tangency portfolio](efficient_frontier.md)
- [Covariance shrinkage](covariance_shrinkage.md)
- [Risk parity](risk_parity.md)
- [Transaction costs and rebalancing](transaction_costs_and_rebalancing.md)

## Free resources
- [Portfolio foundations resources](../../resources/portfolio_foundations.md) — MIT OCW's Portfolio Theory series covers mean/variance and the tangency portfolio directly
