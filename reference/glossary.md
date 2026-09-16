# Glossary

A fast look-up for vocabulary used across this curriculum — one line per
term, not a substitute for the full reference page it links to. If a term
you need isn't here, check [the reference index](index.md) directly; not
every page has a glossary entry, but every glossary entry has a page.

## Portfolio foundations

- **Portfolio return** — the weighted-average return of a portfolio's holdings, `w'r`. [More →](concepts/portfolio_return.md)
- **Covariance** — how two assets' returns move together; the off-diagonal entries of a covariance matrix. [More →](concepts/covariance.md)
- **Portfolio volatility** — `sqrt(w'Sigma*w)`, the standard deviation of portfolio return. [More →](concepts/portfolio_volatility.md)
- **Risk contribution** — how much of total portfolio volatility each position accounts for; splits into marginal (MCR) and component (CR). [More →](concepts/risk_contribution.md)
- **MCTE / CCTE** — marginal/component contribution to *tracking error* — the same idea as risk contribution, but against a benchmark instead of in absolute terms. [More →](concepts/mcte_and_group_risk.md)
- **Group risk decomposition** — aggregating position-level risk contribution by sector, country, or any other label. [More →](concepts/mcte_and_group_risk.md)
- **Sharpe ratio** — excess return per unit of total volatility, `(mean(r) - rf) / std(r)`. [More →](concepts/sharpe_ratio.md)
- **Downside deviation** — like volatility, but counting only shortfalls below a target — the denominator of the Sortino ratio. [More →](concepts/downside_risk.md)
- **Realized (ex-post) risk** — volatility or tracking error measured from an actual return history, as opposed to predicted from a covariance matrix (ex-ante). [More →](concepts/downside_risk.md)
- **Drawdown** — the peak-to-trough decline in cumulative portfolio value. [More →](concepts/drawdown.md)
- **Benchmark basics** — active weight (`w_p - w_b`), active return, and the vocabulary of benchmark-relative investing. [More →](concepts/benchmark_basics.md)
- **Tracking error (TE)** — the volatility of active return, `sqrt(a'Sigma*a)`. [More →](concepts/tracking_error.md)

## Optimization

- **Mean-variance optimization (MVO)** — choosing portfolio weights to maximize `mu'w - (lambda/2)*w'Sigma*w`, the classic return-vs-risk tradeoff. [More →](concepts/mean_variance_optimization.md)
- **Efficient frontier** — the curve of portfolios offering the lowest risk for each level of expected return. [More →](concepts/efficient_frontier.md)
- **Global minimum variance (GMV)** — the single lowest-volatility point on the frontier, ignoring expected return entirely. [More →](concepts/efficient_frontier.md)
- **Tangency portfolio** — the frontier point with the highest Sharpe ratio; every investor's optimal risky-asset mix under Tobin separation. [More →](concepts/efficient_frontier.md)
- **Minimum tracking error** — the benchmark-relative optimization analogue of GMV: weights that minimize active risk instead of absolute risk. [More →](concepts/efficient_frontier.md)

## Active management

- **Information ratio (IR)** — active return per unit of active risk, `active_return / tracking_error`. [More →](concepts/information_ratio.md)
- **Information coefficient (IC)** — the correlation between a manager's forecasts and what actually happened; the raw measure of forecasting skill. [More →](concepts/information_coefficient.md)
- **Breadth (BR)** — the number of independent investment bets; correlated bets count for less than their raw number (`effective_breadth`). [More →](concepts/fundamental_law.md)
- **Transfer coefficient (TC)** — how well real-world constraints let a manager implement their unconstrained-optimal bets; 1.0 = no cost from constraints. [More →](concepts/fundamental_law.md)
- **Fundamental Law of Active Management** — `IR ~= IC * sqrt(BR) * TC`, linking skill, opportunity, and implementation into one expected-IR estimate. [More →](concepts/fundamental_law.md)
- **Active share** — half the sum of absolute active weights; how much of a portfolio differs from its benchmark by market value. [More →](equity/active_share.md)

## Risk models

- **Factor model** — decomposing return/risk into common (factor) and idiosyncratic (specific) pieces, `Sigma = B F B' + D`. [More →](concepts/factor_risk.md)
- **Factor exposure** — a portfolio's sensitivity to a given factor, `w'B`. [More →](concepts/factor_risk_contribution.md)
- **Value at Risk (VaR)** — the loss not expected to be exceeded over a horizon at a given confidence level. [More →](concepts/value_at_risk.md)
- **Expected Shortfall (ES)** — the average loss *given* that VaR is breached; always worse than VaR at the same confidence. [More →](concepts/value_at_risk.md)
- **Stress testing / scenario analysis** — "what happens under this specific, named shock," as distinct from VaR's statistical-confidence framing. [More →](concepts/stress_testing.md)
- **Look-ahead bias** — using a value in a decision dated before that value was published; usually a *revision*, not a future price. [More →](concepts/backtesting_biases.md)
- **Survivorship bias** — measuring only the names still in the dataset, so defaults and closures never drag the average down. [More →](concepts/backtesting_biases.md)
- **Point-in-time data / vintage** — the dataset exactly as it stood on a given date; what a replayable backtest must read instead of today's revised series. [More →](concepts/backtesting_biases.md)

## Fixed income

- **Accrued interest** — coupon earned by the seller since the last payment date, added to the quoted price at settlement. [More →](fixed_income/accrued_interest_and_settlement.md)
- **Clean price / dirty price** — the quoted price versus the price actually paid (clean + accrued). [More →](fixed_income/accrued_interest_and_settlement.md)
- **Day-count convention** — the rule (30/360, ACT/360, ACT/365, ACT/ACT) converting dates to a year-fraction for accrual; part of the bond's terms, not a formatting choice. [More →](fixed_income/accrued_interest_and_settlement.md)
- **Settlement date** — the date cash and bond actually change hands, and the date accrued interest is measured to. [More →](fixed_income/accrued_interest_and_settlement.md)
- **Duration** — the sensitivity of a bond's price to a small yield change, in years. [More →](fixed_income/duration.md)
- **DV01** — the dollar price change of a bond for a 1bp yield move; duration expressed in dollars, not years. [More →](fixed_income/dv01.md)
- **Convexity** — the second-order (curvature) correction to the duration approximation. [More →](fixed_income/convexity.md)
- **Key-rate duration (KRD)** — sensitivity to a yield change at one specific point on the curve, holding the rest fixed. [More →](fixed_income/key_rate_duration.md)
- **Spread duration** — a credit bond's price sensitivity to a change in its spread, holding the underlying rate curve fixed. [More →](fixed_income/spread_duration.md)
- **Z-spread** — the constant spread added to the zero curve that reprices a bond to its market price. [More →](fixed_income/z_spread.md)
- **OAS (option-adjusted spread)** — Z-spread with the value of an embedded option stripped out. [More →](fixed_income/oas.md)
- **CDS (credit default swap)** — an instrument that pays out on an issuer's default; the CDS-bond basis compares its implied spread to the cash bond's. [More →](fixed_income/cds_and_basis.md)
- **Prepayment (CPR / SMM / PSA)** — the rate at which mortgage borrowers repay principal early, and the standard conventions for quoting that speed. [More →](fixed_income/prepayment_models.md)
- **Effective duration** — numerical (bump-and-reprice) duration, needed when price isn't a closed-form function of yield (e.g. MBS). [More →](fixed_income/effective_duration.md)
- **Negative convexity** — a bond (typically MBS) whose duration lengthens when rates rise and shortens when rates fall — the opposite of normal convexity. [More →](fixed_income/mbs_convexity.md)
- **Carry** — the funding-adjusted income earned from holding a bond over time, `(running_yield - financing_rate) * horizon_years`. [More →](fixed_income/carry_and_rolldown.md)
- **Rolldown** — the price gain (or loss) from a bond aging into a shorter point on an unchanged yield curve. [More →](fixed_income/carry_and_rolldown.md)
- **Repo / specialness** — repurchase agreements are how a bond position is actually financed; "special" means a specific bond's repo rate trades below general collateral because it's in unusually high demand to borrow. [More →](fixed_income/repo_and_financing.md)
- **On-the-run / off-the-run** — the most recently auctioned Treasury of a given maturity (on-the-run, most liquid) versus every earlier issue of that maturity (off-the-run, usually cheaper for equivalent cash flows). [More →](fixed_income/repo_and_financing.md)
- **TIPS / breakeven inflation** — Treasury Inflation-Protected Securities adjust principal with CPI; breakeven inflation is `nominal_yield - real_yield`, the market's implied inflation expectation. [More →](fixed_income/tips_and_breakevens.md)
- **Leverage / coverage ratios** — `leverage_ratio = total_debt / EBITDA` and `interest_coverage_ratio = EBITDA / interest_expense`, the core fundamental credit-analysis metrics behind bond and loan covenants. [More →](fixed_income/fundamental_credit_analysis.md)
- **Credit index (CDX / iTraxx)** — a basket of single-name CDS trading as one instrument; its basis is the traded spread minus the weighted-average (intrinsic) spread of its constituents. [More →](fixed_income/credit_indices.md)
- **Leveraged loan** — senior secured, floating-rate debt from a below-investment-grade borrower, priced on a discount-margin basis rather than a fixed yield. [More →](fixed_income/leveraged_loans.md)
- **TBA (to-be-announced) / dollar roll** — generic forward trading of agency MBS without specifying exact pools; a dollar roll sells near-month and buys back far-month, usually at a lower ("dropped") price, functioning as short-term financing. [More →](fixed_income/tba_and_dollar_roll.md)
- **Specified pool / pay-up** — an identified MBS pool traded for its specific collateral characteristics (e.g. low loan balance), commanding a price premium over generic TBA for more predictable prepayment. [More →](fixed_income/specified_pools.md)
- **CMO / REMIC, PAC / support tranche** — a CMO carves one MBS pool into multiple tranches with different principal-payment priority; a PAC tranche gets a predictable schedule within a prepayment band, a support tranche absorbs the resulting variability. [More →](fixed_income/cmo_remic_structuring.md)

## Equity

- **Dividend discount model (DDM)** — valuing a share as the present value of its future dividends. [More →](equity/dividend_discount_model.md)
- **CAPM / beta** — the Capital Asset Pricing Model prices required return as `rf + beta*(market_return - rf)`; beta is systematic risk relative to the market. [More →](equity/capm_and_beta.md)
- **Equity factor investing** — targeting stock returns through style characteristics (value, momentum, quality, size, low-vol) rather than single-market beta alone. [More →](equity/equity_factor_investing.md)
- **Shareholder yield** — dividend yield plus buyback yield; the total cash a company returns to shareholders. [More →](equity/shareholder_yield.md)

## FX

- **Covered interest parity (CIP)** — the forward FX rate is a mechanical function of the two currencies' interest-rate differential, `F = S * (1 + r_domestic*T) / (1 + r_foreign*T)`, not an independent forecast of future spot. [More →](fx/spot_and_forward.md)
- **Cross-currency basis** — the gap between the actual market forward and the forward pure CIP implies; persistently nonzero in practice due to funding constraints and dollar-funding demand. [More →](fx/cross_currency_basis.md)
- **FX carry** — the interest-rate differential earned (or paid) holding a foreign currency unhedged, `r_foreign - r_domestic`; hedging removes it along with the currency risk. [More →](fx/fx_carry.md)

## Commodities

- **Roll yield / contango / backwardation** — the return from replacing an expiring futures contract with the next-dated one; positive in backwardation (near price above far), negative in contango (near price below far). [More →](commodities/roll_yield.md)

## Attribution and implementation

- **Brinson attribution** — decomposing active return into allocation, selection, and interaction effects. [More →](concepts/brinson_attribution.md)
- **Carry / curve / spread decomposition** — the fixed-income-specific version of attribution, splitting return into what you earned for waiting (carry), curve moves, and spread moves. [More →](concepts/fixed_income_attribution.md)
- **Turnover** — how much of a portfolio is traded to move from current to target weights. [More →](concepts/transaction_costs_and_rebalancing.md)

## Advanced portfolio construction

- **Covariance shrinkage** — blending a noisy sample covariance matrix toward a more stable target to reduce estimation error. [More →](concepts/covariance_shrinkage.md)
- **Black-Litterman** — combining a market-implied equilibrium prior with an investor's own views into posterior expected returns. [More →](concepts/black_litterman.md)
- **Risk parity** — allocating capital so every position contributes equally to total risk, rather than equal capital weight. [More →](concepts/risk_parity.md)

## Working with this repo

- **Ex-ante vs. ex-post** — forward-looking (predicted from a model, e.g. a covariance matrix) vs. backward-looking (measured from what actually happened). Comes up throughout risk: `portfolio_volatility` is ex-ante, `realized_volatility` is ex-post.
- **PREDICT / MANUAL FIRST / HAND CALCULATION / ORAL CHECK** — this repo's own notebook vocabulary for its learning cycle; see `notebooks/foundations/00_orientation.ipynb` and `AGENTS.md`.
- **Conceptual-only** — a topic this repo deliberately explains but doesn't implement in code, with a stated reason why (e.g. OAS, hierarchical risk parity). Not a gap — a documented scope decision.
