# Agency MBS Pass-Throughs

## One-line definition
A pool of mortgages where scheduled principal, interest, and any
prepayments are passed straight through to investors pro rata.

## Mechanics
`mortgage_amortization_schedule` (in `src/pm/fixed_income/mbs.py`) gives
the scheduled (no-prepayment) amortization. `apply_prepayment` overlays a
prepayment assumption (an SMM per period) on top of it to get the actual
principal paydown investors receive.

## Why PMs care
Unlike a bullet bond, a pass-through's cash-flow timing is uncertain —
it depends on borrower behavior (refinancing, moving, default), not just
a fixed schedule. That uncertainty is the whole story of MBS risk.

## Common mistakes
- Pricing the scheduled amortisation as if it were the cash flow.
  `mortgage_amortization_schedule` gives the no-prepayment path;
  investors receive that plus prepayments, and the difference is the
  entire point of the instrument.
- Treating an SMM as a CPR. SMM is the monthly rate, CPR the annualised
  one — `single_monthly_mortality` converts, and confusing the two
  misstates paydown by an order of magnitude.
- Assuming a constant prepayment speed. Speeds respond to the
  refinancing incentive, which moves with rates. A single SMM is a
  scenario, not a forecast — see [Prepayment models](prepayment_models.md).
- Using ordinary duration. Cash-flow timing changes when rates move, so
  the price/yield relationship turns negatively convex;
  [effective duration](effective_duration.md) is the measure that
  accounts for it.

## Related
- [Prepayment models](prepayment_models.md)
- [Effective duration](effective_duration.md)
- [TBA and the dollar roll](tba_and_dollar_roll.md)
- [Specified pools](specified_pools.md)
