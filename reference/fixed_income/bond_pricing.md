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

## Related
- [Accrued interest and settlement](accrued_interest_and_settlement.md)
- [Duration](duration.md)
- [DV01](dv01.md)
- [Curve construction](curve_construction.md)
- [TIPS and breakeven inflation](tips_and_breakevens.md)
- [Convertible bonds](convertible_bonds.md)
