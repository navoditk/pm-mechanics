# Performance Measurement: Time-Weighted vs. Money-Weighted Return

## One-line definition
Time-weighted return (TWR) measures a manager's skill independent of
when clients moved money in or out; money-weighted return (MWR, also
called the dollar-weighted return or IRR) measures the investor's actual
realized return on the capital they actually had at risk. They diverge
whenever cash flows happen mid-period, and the divergence isn't a bug in
either one — they're answering different questions.

## Formula
**TWR** — geometrically link each sub-period's return (a sub-period ends
every time an external cash flow happens):
`TWR = (1+r_1) * (1+r_2) * ... * (1+r_n) - 1`

This repo already has this: `pm.returns.cumulative_return` computes
exactly this geometric link — TWR isn't a new calculation, it's the
existing function applied to sub-periods split at each cash flow.

**MWR** — the constant periodic rate `r` that sets the net present value
of every cash flow (including the starting investment and ending value)
to zero:
`sum(cash_flow_i / (1+r)^time_i) = 0`

`pm.returns.money_weighted_return(cash_flows, times)` solves this
numerically (bisection), since there's no closed form for more than two
cash flows.

## Why PMs care
GIPS (the industry-standard performance-presentation rules) requires
time-weighted return for composite reporting precisely because it
isolates manager skill from client-driven cash-flow timing — a manager
shouldn't be credited or blamed for a client depositing right before a
rally or right before a crash. But TWR is the wrong number for an
*investor* asking "what did I actually earn on my money?" — that
question is answered by MWR, which is exactly as sensitive to timing and
size of contributions as the investor's own bank balance is. A PM
reporting composite performance uses TWR; a PM explaining a specific
client's actual realized experience uses MWR — conflating the two is a
common, misleading mistake.

## Worked example
The canonical case where they sharply diverge: an investor starts with
$100. By the end of year 1, the portfolio doubles to $200 (period-1
return = +100%) — the investor then contributes another $200, bringing
the total invested to $400. By the end of year 2, the portfolio falls
back to $200 (period-2 return = -50%).

`TWR = (1+1.00) * (1-0.50) - 1 = 0%` — a wash, using `cumulative_return`.

`MWR`: cash flows of -100 (t=0, initial investment), -200 (t=1,
additional contribution), +200 (t=2, ending value) — solving
`money_weighted_return` gives **r ≈ -26.79%**
(`tests/test_returns.py::test_money_weighted_return_classic_twr_divergence_example`).

The manager's skill (as TWR sees it) was neutral across the two years.
But the investor's actual experience was strongly negative, because they
had four times as much capital exposed during the losing year as during
the winning one — MWR captures exactly that, TWR by design does not.

## Why full GIPS composite construction isn't implemented in `src/pm`
GIPS composite requirements — asset-weighting individual portfolio
returns into a firm-wide composite, minimum-size and significant-cash-
flow policies, verification procedures, and the disclosure/presentation
rules themselves — are a compliance and process framework layered on top
of the return calculations above, not a new formula. `cumulative_return`
and `money_weighted_return` are the actual computational core GIPS
requires; the rest is organizational policy this repo's "small
transparent function" style doesn't attempt to encode.

## Common mistakes
- reporting MWR when GIPS (or a mandate) requires TWR, because MWR
  "looks like" the more intuitive number — it answers a different
  question and isn't a substitute
- assuming TWR and MWR only diverge in extreme cases — any mid-period
  cash flow at all creates *some* divergence; the classic example above
  is chosen to make it dramatic, not because dramatic divergence is rare
- treating `money_weighted_return`'s brentq solve as guaranteed to
  converge for any cash-flow pattern — it assumes a single real root
  (true for the typical one-sign-change pattern of contributions then a
  final withdrawal), which isn't guaranteed for cash flows with multiple
  sign changes

## Related
- [Sharpe ratio](sharpe_ratio.md)
- [Brinson attribution](brinson_attribution.md)
- [Backtesting biases](backtesting_biases.md)
- [Liability-driven investing](liability_driven_investing.md)

## Free resources
- [Time-weighted return — Wikipedia](https://en.wikipedia.org/wiki/Time-weighted_return) — the formula and the TWR-vs-MWR distinction, with a worked example
- [Overview of the Global Investment Performance Standards — CFA Institute](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-of-the-global-investment-performance-standards) — why GIPS mandates time-weighted return and how composites are built
