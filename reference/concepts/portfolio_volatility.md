# Portfolio Volatility

## Formula
`sigma_p = sqrt(w^T Sigma w)`

## Why PMs care
It summarizes total portfolio return dispersion under the covariance model.

## Two-asset form
`sigma_p^2 = w1^2 sigma1^2 + w2^2 sigma2^2 + 2 w1 w2 rho12 sigma1 sigma2`

## Code recipe
```python
def portfolio_volatility(weights, covariance):
    w = np.asarray(weights, float)
    cov = np.asarray(covariance, float)
    return float(np.sqrt(w @ cov @ w))
```

## Invariant
Variance should be non-negative up to numerical tolerance.

## Common mistakes
- Averaging the holdings' individual volatilities. That ignores the
  cross terms entirely and overstates risk for any portfolio that is not
  perfectly correlated — the diversification benefit lives in
  `2 w1 w2 rho12 sigma1 sigma2`, not in the diagonal.
- Feeding in a covariance matrix built from a different periodicity than
  the one you report in. Monthly covariance gives monthly volatility;
  annualising means scaling by `sqrt(periods_per_year)`, not by
  `periods_per_year`.
- Reading this as *realized* risk. It is the volatility the covariance
  model predicts. Compare it against `realized_volatility` on an actual
  return history before trusting it — see
  [Downside deviation and realized risk](downside_risk.md).
- Treating a small negative variance from floating-point error as a bug
  in the maths rather than in the matrix. A genuinely non-PSD covariance
  is an input problem; see [Covariance shrinkage](covariance_shrinkage.md).

## Related
- [Covariance](covariance.md)
- [Risk contribution](risk_contribution.md)
