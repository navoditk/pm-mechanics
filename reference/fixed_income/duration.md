# Duration

## One-line definition
A first-order measure of a bond or fixed-income portfolio's sensitivity to changes in yield/rates.

## Price approximation
`dP/P ≈ -D_mod * dy`

## Interpretation
Modified duration of 5 implies approximately a 5% price decline for a 100 bp parallel yield increase, before convexity and other effects.

## Why PMs care
Duration converts rate views and risk limits into portfolio sensitivity.

## Common mistakes
- Using it for a large yield move. The approximation is first-order and
  degrades quadratically; past roughly 50-100bp the missing
  [convexity](convexity.md) term matters.
- Assuming a parallel shift. Duration prices one number moving the whole
  curve. A steepening or flattening needs
  [key-rate duration](key_rate_duration.md), which is precisely the
  distinction the two measures exist to draw.
- Confusing Macaulay with modified duration. Macaulay is a
  time-weighted average maturity in years; modified is the price
  sensitivity, `Macaulay / (1 + ytm/frequency)`.
- Applying rate duration to a spread move. Credit spread sensitivity is
  [spread duration](spread_duration.md), a separate input — this repo's
  scenario tool reads a different field for each.

## Related
- [DV01](dv01.md)
- [Convexity](convexity.md)
- [Key-rate duration](key_rate_duration.md)
- [Effective duration](effective_duration.md)
- [Carry and rolldown](carry_and_rolldown.md)
