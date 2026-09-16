# Backtesting Biases and Point-in-Time Data

## One-line definition
The systematic ways a backtest flatters a strategy by using information that
was not actually available at the moment the decision would have been made.

## The three that matter most

**Look-ahead bias** — using a value in a decision dated before that value
existed. The classic case is not a future price but a *revised* one: GDP,
earnings, index membership, and credit ratings are all restated after
publication. A backtest that reads today's database at an earlier date is
silently using the revision.

**Survivorship bias** — measuring a universe that only contains what
survived. Funds that closed, issuers that defaulted, and names delisted from
an index leave the dataset, so the remaining sample looks better than the
opportunity set actually was.

**Stale data** — carrying a last-known price forward through a gap. This
does not raise returns so much as suppress measured volatility and
correlation, which makes risk look lower and Sharpe look higher.

## Point-in-time data and vintage
A **vintage** is the dataset exactly as it stood on a given date. Point-in-time
discipline means a decision dated `t` may only read the vintage published at
or before `t`. Storing both an `observation_date` (what period the number
describes) and a `vintage` (when it was published) is what makes a backtest
replayable; a single-date series cannot distinguish the two, and so cannot
prove it avoided look-ahead.

## Worked intuition
Ten bonds, one defaults and leaves the index. The nine survivors average
+4%; the defaulted name returned −60%. Report the survivors and the universe
earned 4%. Include the exit and it earned `(9*4 + (-60)) / 10 = -2.4%`. The
strategy did not change — only which names the dataset still contained.

## Why PMs care
These biases inflate exactly the statistics used to justify a mandate:
return, Sharpe, information ratio, hit rate. They are also invisible in the
output — a biased backtest produces clean, plausible numbers. The only
defence is procedural: knowing which vintage fed which decision.

## Why this page has no formula
There is no calculation to implement. Every bias here is a property of *how
the dataset was assembled*, not of the arithmetic applied to it — the
worked example above is ordinary averaging over two different universes.
The discipline is in the data layer, and this repo's data layer is a handful
of static mock CSVs with no vintage dimension, so there is nothing here to
compute against. Treat this page as a checklist to run before trusting any
backtest, including one built from this repo's own tools.

The governed, provenance-tracked version of this problem — vintage-aware
connectors, observation/vintage envelopes, point-in-time replay — is built
out in [agentic-pm-lab](https://github.com/navoditk/agentic-pm-lab), which
is where the data layer lives.

## Related
- [Performance measurement](performance_measurement.md)
- [Information coefficient](information_coefficient.md)
- [Liquidity](liquidity.md)
- [Transaction costs and rebalancing](transaction_costs_and_rebalancing.md)
