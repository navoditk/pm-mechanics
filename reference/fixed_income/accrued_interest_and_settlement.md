# Accrued Interest and Settlement

## One-line definition
The gap between a bond's quoted (clean) price and the cash a buyer actually
pays (dirty price), made up of interest the seller has earned but not yet
been paid.

## Formula
```
accrued    = face * coupon_rate / frequency * (elapsed / full period)
dirty      = clean + accrued
invoice    = face / 100 * dirty          # quotes are per 100 of face
```
`elapsed` and `full period` are both measured with the bond's **day-count
convention**, so the ratio is the share of the coupon period that has passed.

## Day-count conventions
The convention is part of the instrument's terms, not a formatting detail.
The same dates and the same coupon give different accrued interest under
each one:

| Convention | Elapsed days | Year basis |
|---|---|---|
| 30/360 | every month treated as 30 days | 360 |
| ACT/360 | actual calendar days | 360 |
| ACT/365 | actual calendar days | 365 |
| ACT/ACT | actual calendar days | 365, or 366 in a leap year |

30/360 carries two end-of-month adjustments, and their **order matters**: a
start date on the 31st collapses to the 30th first, and only then does an end
date on the 31st collapse. Adjusting the end date first gives a different
answer when both fall on a 31st — `tests/test_settlement.py` pins this.

## Interpretation
Buy a 5% semi-annual bond exactly halfway through its coupon period and you
pay the quoted price plus half a coupon — 1.25 per 100 of face. You get the
whole 2.50 coupon at the next payment date, so the accrued payment simply
compensates the seller for the part of the period they held it. Accrued is
zero on a coupon date and rises linearly to a full coupon just before the
next one.

## Why PMs care
Every other page in this section works in clean prices, because that is what
gets quoted. Cash does not move in clean prices. Position values, settlement
amounts, and any reconciliation against a custodian or counterparty need the
dirty price — and a wrong day-count convention produces a number that is
confidently wrong rather than obviously broken, which is exactly the kind of
error that survives review.

## In this repo
`src/pm/fixed_income/settlement.py` — `day_count_fraction`,
`accrued_interest`, `dirty_price`, `clean_price`, `invoice_amount`. An
unknown convention raises rather than silently defaulting, on the principle
that a wrong convention is a wrong number.

`ACT/ACT` here is the simple year-basis approximation, not full ISDA
ACT/ACT, which splits a period across year boundaries. That matters for
periods spanning a year end; the docstring says so rather than implying
otherwise.

## Common mistakes
- Assuming a day-count convention instead of reading it from the
  instrument's terms. `day_count_fraction` raises on an unknown
  convention for exactly this reason — a wrong convention produces a
  confidently wrong number rather than an obvious failure.
- Applying the 30/360 end-of-month adjustments in the wrong order. The
  start date collapses from the 31st to the 30th *first*; only then may
  the end date. Reversing it changes the answer when both fall on a
  31st, and `tests/test_settlement.py` pins the case.
- Using this module's `ACT/ACT` where full ISDA ACT/ACT is required. This
  is the simple year-basis approximation and does not split a period
  across a year boundary.
- Adding accrued interest to a price already quoted dirty, producing a
  double count. Check which convention the quote is on before adjusting.

## Related
- [Bond pricing](bond_pricing.md)
- [Repo and financing](repo_and_financing.md)
- [Carry and rolldown](carry_and_rolldown.md)
- [Duration](duration.md)
