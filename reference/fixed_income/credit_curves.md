# Credit Curves, IG, and HY

## One-line definition
The term structure of credit spread by tenor for a given issuer or rating
bucket — same idea as a Treasury zero curve, applied to credit spread.

## Construction
Reuse `interpolate_zero_rate` from `src/pm/fixed_income/curve.py` on
spread points instead of yield points — a credit curve is interpolated
the same way a rates curve is.

## Vocabulary
- **Investment grade (IG)**: rated BBB-/Baa3 or above — lower spread,
  lower default probability.
- **High yield (HY)**: rated BB+/Ba1 or below — higher spread, higher
  default probability, more convex to spread widening.
- IG and HY often move together directionally but with very different
  magnitudes — see `use_cases/spread_shock/README.md`.

## Why PMs care
Credit curve shape (steep vs. flat, IG vs. HY) reflects the market's view
of near-term vs. long-term default risk for that issuer or sector.

## Common mistakes
- Interpolating spread the same way for IG and HY without comment. The
  mechanics are identical, but HY spreads are far more convex to
  widening, so a linear interpolation between sparse HY points
  understates the move more than it does for IG.
- Reading curve steepness as a pure default-timing view. Shape also
  reflects liquidity, issuance, and index composition, not just the
  market's term structure of default risk.
- Treating a rating bucket as an issuer curve. A BBB sector curve is an
  average; a specific issuer can trade far off it, and pricing an issuer
  off the bucket hides exactly the idiosyncratic risk you are paid for.
- Discounting with spread alone. A credit-risky bond is priced off the
  risk-free curve *plus* the spread — see [Z-spread](z_spread.md).

## Related
- [Curve construction](curve_construction.md)
- [Z-spread](z_spread.md)
- [Default and recovery](default_recovery.md)
- [Sovereign and EM debt](sovereign_and_em_debt.md)
