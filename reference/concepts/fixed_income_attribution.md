# Fixed-Income Return Attribution: Carry, Curve, Spread

## One-line definition
Splitting a bond portfolio's realized return into carry (income earned by
holding), curve/duration effect (P&L from rate moves), and spread effect
(P&L from credit spread moves) — Brinson's sector/security split doesn't
fit fixed income well, since the same bond can be over/underweight
*and* have a rate view *and* a credit view simultaneously.

## Formula
No new math — this combines pieces already built elsewhere:
- carry ≈ yield earned over the holding period
- curve effect: `key_rate_return_approximation` (`src/pm/fixed_income/curve.py`)
- spread effect: `spread_pnl` (`src/pm/fixed_income/credit.py`)

`fixed_income_return_decomposition(carry, curve_effect, spread_effect)` in
`src/pm/attribution.py` just labels and totals them for reporting.

## Why PMs care
A fixed-income portfolio can show a flat total return while carry, curve,
and spread are all large and offsetting — knowing which is true changes
what you'd do next (e.g. a curve loss offset by carry is very different
from a spread loss offset by curve).

## Common mistakes
- Expecting the three effects to sum exactly to realized return. Carry,
  curve, and spread are each approximations built on duration measures;
  the residual is the part the first-order model does not explain, and
  a large residual is information rather than an error to hide.
- Double-counting carry and rolldown. Rolldown is a price effect from
  moving along an unchanged curve and belongs in the curve term, not in
  carry — see [Carry and rolldown](../fixed_income/carry_and_rolldown.md).
- Attributing a spread move to credit when the benchmark curve itself
  moved. Spread is measured *against* a curve; if the curve shifted
  under it, part of the apparent spread effect is a curve effect.
- Reaching for Brinson instead. Sector/security attribution assumes
  allocation and selection are separable, which does not hold when one
  bond carries a rate view and a credit view at once.

## Related
- [Brinson attribution](brinson_attribution.md)
- [Key-rate duration](../fixed_income/key_rate_duration.md)
- [Spread duration](../fixed_income/spread_duration.md)
