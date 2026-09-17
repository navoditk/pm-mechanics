# Bond Pricing and Yield to Maturity

## One-line definition
The price of a bond is the present value of its future cash flows,
discounted at its yield to maturity (YTM).

## Formula
`P = sum_t CF_t / (1 + ytm/frequency)^t`

where `CF_t` is the coupon (or coupon + face at maturity) paid at period `t`.

## Interpretation
A bond priced at par (`P = face`) has `ytm = coupon_rate`. Price and yield
move inversely — this is the mechanism duration approximates linearly.

## Why PMs care
Every other fixed-income sensitivity (duration, DV01, convexity) is a
derivative of this pricing relationship.

## Common mistakes
- Reporting this price as what a buyer pays. It is the *clean* price;
  settlement adds accrued interest. See
  [Accrued interest and settlement](accrued_interest_and_settlement.md).
- Mixing the yield's compounding frequency with the coupon frequency.
  `ytm/frequency` assumes they match; a semi-annual bond quoted on an
  annual yield needs converting first.
- Assuming one yield is the right discount rate for every cash flow.
  YTM is a single internal rate; a curve-based present value discounts
  each flow at its own tenor and will not agree exactly. See
  [Curve construction](curve_construction.md).
- Treating price/yield as linear. It is convex — duration is only the
  first-order term, which is why [convexity](convexity.md) exists.

## Related
- [Accrued interest and settlement](accrued_interest_and_settlement.md)
- [Duration](duration.md)
- [DV01](dv01.md)
- [Curve construction](curve_construction.md)
- [TIPS and breakeven inflation](tips_and_breakevens.md)
- [Convertible bonds](convertible_bonds.md)
