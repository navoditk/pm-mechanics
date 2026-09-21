# Agentic Analytics Evals

Manually-run checklist for `/pm-query` (`skills/pm-query/SKILL.md`).
There is no automated harness for skill-routing behavior — that needs a
live agent test rig this repo doesn't have — so this stays an honest,
human-runnable checklist rather than a fake `pytest` suite. Each row's
expected output was computed and verified directly against `src/pm`
(not hand-derived) before being written here.

To run: ask `/pm-query` each question, and confirm (a) it calls the
listed function with the listed inputs, (b) the output matches, and
(c) it cites the function/module and a reference page, not just a bare
number.

| Query | Expected function | Inputs | Expected output |
|---|---|---|---|
| "DV01 of a 5-year 5% semiannual bond at a 4% yield?" | `pm.fixed_income.duration.dv01` | `ytm=0.04, face=100, coupon_rate=0.05, years=5, frequency=2` | `0.04609` (≈) |
| "Sharpe ratio of returns 2%, 4%, 3%, risk-free 0%, annual periods?" | `pm.returns.sharpe_ratio` | `returns=[0.02,0.04,0.03], risk_free_rate=0.0, periods_per_year=1` | `3.0` |
| "95% parametric VaR of a $1,000,000 portfolio with 2% daily vol?" | `pm.risk.parametric_var` | `portfolio_value=1_000_000, volatility=0.02, confidence=0.95` | `32897.07` (≈) |
| "1-year FX forward for spot 1.10, USD rate 5%, EUR rate 3%?" | `pm.fx.fx_forward_rate` | `spot=1.10, domestic_rate=0.05, foreign_rate=0.03, years=1` | `1.121359` (≈) |
| "Risk-parity weights for two uncorrelated assets at 20% and 10% vol?" | `pm.robust.risk_parity_weights` | `covariance=[[0.04,0],[0,0.01]]` | `[0.3333, 0.6667]` (≈) |
| "Roll yield if the near contract is $80 and the far contract is $78?" | `pm.commodities.roll_yield` | `near_price=80, far_price=78` | `0.02564` (≈, backwardation) |
| "Gordon growth value of a stock with a $2 next dividend, 9% required return, 4% growth?" | `pm.equity.valuation.gordon_growth_value` | `dividend_next=2.0, required_return=0.09, growth_rate=0.04` | `40.0` |
| "Beta of a stock whose returns move 1.5x the market's?" | `pm.equity.capm.beta` | `stock_returns=[0.015,0.03,-0.015,0.045,0.0], market_returns=[0.01,0.02,-0.01,0.03,0.0]` | `1.5` |
| "Information ratio if portfolio returns are 3%/5%/2% and benchmark returns are 1%/2%/1%, unannualized?" | `pm.active.information_ratio` | `portfolio_returns=[0.03,0.05,0.02], benchmark_returns=[0.01,0.02,0.01], periods_per_year=1` | `2.0` |
| "Expected information ratio for a manager with a 0.05 IC and 100 independent bets, no constraints?" | `pm.active.fundamental_law_ir` | `information_coefficient_value=0.05, breadth_value=100, transfer_coefficient_value=1.0` | `0.5` |
| "Unconstrained tangency portfolio for two uncorrelated assets, mu=[8%,5%], vol=[20%,10%], risk-free 2%?" | `pm.optimization.max_sharpe` | `expected_returns=[0.08,0.05], covariance=[[0.04,0],[0,0.01]], risk_free_rate=0.02, long_only=False` | `[0.3333, 0.6667]` (≈) |
| "Carry on a 5Y bond yielding 4.00% financed at 3.00% repo, held 1 year?" | `pm.fixed_income.carry.carry_return` | `coupon_income=4.0, price=100.0, financing_rate=0.03, horizon_years=1.0` | `0.01` |
| "Breakeven inflation with nominal 4.5% and TIPS real yield 2.0%?" | `pm.fixed_income.linkers.breakeven_inflation` | `nominal_yield=0.045, real_yield=0.02` | `0.025` |
| "Leverage ratio for an issuer with $300M debt and $100M EBITDA?" | `pm.fixed_income.credit.leverage_ratio` | `total_debt=300, ebitda=100` | `3.0` |
| "Index basis if 5 CDS constituents (80,90,100,70,110bp) trade equal-weighted and the index itself trades at 95bp?" | `pm.fixed_income.credit.index_intrinsic_spread` then `index_basis` | `constituent_spreads=[80,90,100,70,110]` → `intrinsic=90.0`; `index_basis(95, 90)` | `5.0` |
| "Implied financing rate on a dollar roll: $1,000,000 face, 5% coupon, near price 101.00, far price 100.625, 1-month roll?" | `pm.fixed_income.mbs.dollar_roll_implied_financing_rate` | `coupon_income=4166.6667, drop_income=3750.0, near_amount=1010000.0, horizon_years=1/12` | `0.004950` (≈, 0.495%) |
| "Black-Scholes call price: spot 100, strike 100, rate 5%, vol 20%, 1 year to expiry?" | `pm.options.black_scholes_call_price` | `spot=100.0, strike=100.0, rate=0.05, volatility=0.20, time_to_expiry=1.0` | `10.450584` (≈) |
| "Delta of that same call?" | `pm.options.delta_call` | `spot=100.0, strike=100.0, rate=0.05, volatility=0.20, time_to_expiry=1.0` | `0.636831` (≈) |
| "What's the swaption's vega if the swap rate moves 1bp?" | none — conceptual only | — | should say plainly that a real swaption needs an annuity/curve factor `pm.options.black76_call_price` doesn't build, and point to `reference/derivatives/options_on_forwards_and_rates_options.md` rather than approximating one |
| "Money-weighted return for cash flows of -100 at t=0, -200 at t=1, and +200 at t=2?" | `pm.returns.money_weighted_return` | `cash_flows=[-100.0,-200.0,200.0], times=[0.0,1.0,2.0]` | `-0.267949` (≈, the classic TWR-vs-MWR divergence case, where the matching TWR is 0%) |
| "Funded ratio for a plan with $90M assets and $100M liabilities?" | `pm.allocation.funded_ratio` | `assets=90.0, liabilities=100.0` | `0.90` |
| "What's the plan's ideal strategic asset allocation?" | none — conceptual only | — | should say plainly that SAA is this repo's existing optimization tools (`mean_variance_optimization`, `black_litterman_posterior`) reapplied at the policy level, not a separate calculation, and ask for the actual capital-market-expectation inputs rather than inventing an allocation |
| "Tax-equivalent yield for a 3% muni, 32% tax bracket?" | `pm.fixed_income.munis.tax_equivalent_yield` | `muni_yield=0.03, tax_rate=0.32` | `0.044118` (≈, 4.41%) |
| "Conversion value and premium for a $1,000 convertible, 20 conversion ratio, stock at $45, bond price 950?" | `pm.fixed_income.convertibles.conversion_value` then `conversion_premium` | `conversion_ratio=20, stock_price=45.0` → `900.0`; `conversion_premium(950.0, 900.0)` | `0.055556` (≈, 5.56%) |
| "What's this preferred stock's fair value: $2 dividend, 8% required return?" | `pm.equity.valuation.gordon_growth_value` | `dividend_next=2.0, required_return=0.08, growth_rate=0.0` | `25.0` |
| "What's the OAS of this callable bond?" | none — conceptual only | — | should say plainly that OAS isn't implemented, and point to `reference/fixed_income/oas.md` rather than approximating one |

## What a passing run looks like

- Every numeric row: the skill actually executes the cited function (via
  `python -c` or similar) rather than stating a number from reasoning.
- The OAS row: the skill declines to fabricate a number and explains why,
  citing the conceptual-only reference page — this is as important a pass
  condition as getting the numeric rows right.
- Every answer names the specific function/module used.
