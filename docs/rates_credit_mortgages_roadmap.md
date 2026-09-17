# Rates, Credit, and Mortgages: Zero to Hero

A single sequenced path through this repo's full fixed-income coverage —
pricing and risk mechanics *and* the practitioner/market-structure layer
on top of it (carry and roll, repo, TIPS, credit indices, fundamental
credit analysis, TBA/dollar roll, specified pools, CMO/REMIC structuring)
— with the reference page, notebook, and one or two verified external
resources for every step. Follow it in order; each tier assumes the ones
before it.

This is the FICC-specific complement to [learning
paths](./learning-paths.md)'s Path B, expanded to the depth the "start
from zero, reach a reasonable level of proficiency" goal actually
requires. Use it manually (read → predict → derive → code → test →
explain, per [getting started](./getting-started.md)) or drive it
interactively with `/pmexpert` — see [the mastery
guide](./mastery-guide.md); `/pmexpert` already walks this exact
curriculum order.

## Before you start

1. `notebooks/foundations/00_orientation.ipynb` — environment check, the
   PREDICT/MANUAL FIRST/ORAL CHECK learning cycle, and the one piece of
   matrix math (`w' Sigma w`) later notebooks assume. Skip this if you've
   already done it.
2. Keep [reference/glossary.md](../reference/glossary.md) open as a
   look-up for unfamiliar terms throughout.
3. `notebooks/fixed_income/08_bond_math.ipynb` — bond pricing and YTM,
   the base every later rates/credit/mortgages concept builds on.

**Free resources:** [PIMCO Fixed Income Education
Center](https://www.pimco.com/ca/en/resources/education-center/fixed-income)
for terminology and framing before diving into any single topic below.

---

## Tier 1 — Rates

### 1.1 Duration, DV01, convexity, key-rate duration
Reference: `reference/fixed_income/duration.md`, `dv01.md`,
`convexity.md`, `key_rate_duration.md`
Notebook: `notebooks/fixed_income/09_duration_curve_risk.ipynb`
Resource: [PIMCO — Understanding
Duration](https://www.pimco.com/us/en/resources/education/understanding-duration)

### 1.2 Curve construction and forward rates
Reference: `reference/fixed_income/curve_construction.md`,
`forward_rates.md`
Notebook: `notebooks/fixed_income/14_curve_construction_forwards.ipynb`
Resource: [CME Group education hub](https://www.cmegroup.com/education/)
— curve bootstrapping intuition and forward rates

### 1.3 Curve trades: steepeners, flatteners, butterflies
Reference: `reference/fixed_income/curve_trades.md`
Notebook: `notebooks/fixed_income/15_curve_trades_scenarios.ipynb`
Resource: [U.S. Treasury Interest Rate
Statistics](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics)
and [FRED](https://fred.stlouisfed.org/) for real curve data to test
trade ideas against

### 1.4 Swaps, swap DV01, swap spreads
Reference: `reference/fixed_income/swap_dv01.md`, `swap_spread.md`
Notebook: `notebooks/fixed_income/16_swaps_and_swap_spreads.ipynb`

### 1.5 Treasury futures and hedging
Reference: `reference/fixed_income/treasury_futures_hedging.md`
Notebook: `notebooks/fixed_income/17_futures_and_hedging.ipynb`
Resource: [CME Group education hub](https://www.cmegroup.com/education/)
— Treasury futures and hedge ratios

### 1.6 Carry and rolldown
Reference: `reference/fixed_income/carry_and_rolldown.md`
Notebook: `notebooks/fixed_income/31_carry_roll_and_financing.ipynb`
Resource: [Carry Roll-Down Explained —
riskhub.org](https://riskhub.org/blogs/carry-roll-down-explained) — the
exact formula and worked example this repo's numbers are checked against

### 1.7 Repo, specialness, on-the-run vs. off-the-run
Reference: `reference/fixed_income/repo_and_financing.md` (conceptual —
repo rate is a market observation, not a formula)
Notebook: `notebooks/fixed_income/31_carry_roll_and_financing.ipynb`
Resources: [On the run (finance) —
Wikipedia](https://en.wikipedia.org/wiki/On_the_run_(finance)); [What's
going on in the US Treasury market, and why does it matter? —
Brookings](https://www.brookings.edu/articles/whats-going-on-in-the-us-treasury-market-and-why-does-it-matter/);
[Money Market Fund Repo and the ON RRP Facility — Federal
Reserve](https://www.federalreserve.gov/econres/notes/feds-notes/money-market-fund-repo-and-the-on-rrp-facility-20231215.html)

### 1.8 TIPS and breakeven inflation
Reference: `reference/fixed_income/tips_and_breakevens.md`
Notebook: `notebooks/fixed_income/31_carry_roll_and_financing.ipynb`
Resources: [TIPS for Inflation Protection — Charles
Schwab](https://www.schwab.com/learn/story/tips-and-inflation-what-to-know-now);
[10-Year Breakeven Inflation Rate (T10YIE) —
FRED](https://fred.stlouisfed.org/series/T10YIE)

**Apply it:** `use_cases/duration_hedging/`,
`use_cases/curve_positioning/`, `use_cases/swap_dv01_hedge/`,
`use_cases/treasury_futures_hedge/` — see
[use_cases/index.md](../use_cases/index.md).

---

## Tier 2 — Credit

### 2.1 Credit spreads and spread duration
Reference: `reference/fixed_income/spread_duration.md`
Notebook: `notebooks/fixed_income/10_credit_spreads.ipynb`

### 2.2 Z-spread and credit curves
Reference: `reference/fixed_income/z_spread.md`,
`credit_curves.md`
Notebook: `notebooks/fixed_income/20_z_spread_and_credit_curves.ipynb`

### 2.3 Default, recovery, hazard rate, CDS, CDS-bond basis
Reference: `reference/fixed_income/default_recovery.md`,
`cds_and_basis.md`
Notebook: `notebooks/fixed_income/21_default_recovery_and_cds.ipynb`

### 2.4 Credit migration
Reference: `reference/fixed_income/credit_migration.md` (conceptual —
full rating-transition matrices are out of scope; see the page for why)

### 2.5 Fundamental credit analysis: leverage, coverage, covenants
Reference: `reference/fixed_income/fundamental_credit_analysis.md`
Notebook: `notebooks/fixed_income/32_fundamental_credit_and_indices.ipynb`
Resources: [Financial Ratios for Credit Analysis — AnalystPrep (CFA
Level
1)](https://analystprep.com/cfa-level-1-exam/fixed-income/financial-ratios-credit-analysis/);
[An Introduction to Covenants in Leveraged Finance Debt —
CredCore](https://credcore.com/insights/an-introduction-to-covenants-in-leveraged-finance-debt)

### 2.6 Credit indices: CDX / iTraxx, intrinsic spread, basis
Reference: `reference/fixed_income/credit_indices.md`
Notebook: `notebooks/fixed_income/32_fundamental_credit_and_indices.ipynb`
Resources: [Credit Default Swap Indices — Financial Edge
Training](https://www.fe.training/free-resources/financial-markets/credit-default-swap-indices/);
[Credit default swap index —
Wikipedia](https://en.wikipedia.org/wiki/Credit_default_swap_index)

### 2.7 Leveraged loans
Reference: `reference/fixed_income/leveraged_loans.md` (conceptual —
floating-rate/discount-margin mechanics differ enough from this repo's
fixed-coupon bond pricing that they aren't coded; see the page for why)
Notebook: `notebooks/fixed_income/32_fundamental_credit_and_indices.ipynb`
Resources: [Leveraged Lending and Collateralized Loan Obligations: FAQs —
Congressional Research
Service](https://www.congress.gov/crs-product/R46096); [Leveraged Credit
Markets: Then and Now — Western & Southern / Fort
Washington](https://www.westernsouthern.com/fortwashington/insights/leveraged-credit-markets)

### 2.8 OAS
Reference: `reference/fixed_income/oas.md` (conceptual only — full
option-adjusted spread requires a term-structure model this repo doesn't
build; the page explains exactly what would be needed)

**Apply it:** `use_cases/spread_shock/` — see
[use_cases/index.md](../use_cases/index.md).

---

## Tier 3 — Securitized / Mortgages

### 3.1 Pass-throughs and amortization
Reference: `reference/fixed_income/pass_throughs.md`
Notebook: `notebooks/fixed_income/22_pass_throughs_and_prepayment.ipynb`

### 3.2 Prepayment: CPR, SMM, PSA
Reference: `reference/fixed_income/prepayment_models.md`
Notebook: `notebooks/fixed_income/22_pass_throughs_and_prepayment.ipynb`

### 3.3 Effective duration and MBS negative convexity
Reference: `reference/fixed_income/effective_duration.md`,
`mbs_convexity.md`
Notebook: `notebooks/fixed_income/23_effective_duration_and_convexity.ipynb`

### 3.4 Non-agency, ABS, CMBS overview
Reference: `reference/fixed_income/non_agency_overview.md` (conceptual —
tranche waterfall modeling is materially bigger than this repo's
pool-level pass-through math; see the page for why)

### 3.5 TBA and the dollar roll
Reference: `reference/fixed_income/tba_and_dollar_roll.md`
Notebook: `notebooks/fixed_income/33_tba_dollar_roll_and_structuring.ipynb`
Resources: [Dollar roll —
Wikipedia](https://en.wikipedia.org/wiki/Dollar_roll); [Using Dollar
Rolls as a Balance Sheet and Earnings Strategy for Banks and Credit
Unions — Doeren
Mayhew](https://www.doeren.com/viewpoint/using-dollar-rolls-as-a-balance-sheet-and-earnings-strategy-for-banks-and-credit-unions)
— the worked example this repo's formula is checked against

### 3.6 Specified pools
Reference: `reference/fixed_income/specified_pools.md` (conceptual —
pay-up is a market-observed premium, not a formula; see the page for why)
Notebook: `notebooks/fixed_income/33_tba_dollar_roll_and_structuring.ipynb`
Resources: [Specified Pool and TBA Trading in the Mortgage Backed
Securities Market — SMU Cox Finance Seminar
Series](https://www.smu.edu/-/media/site/cox/departments/finance/finaseminarseries/tba_specified_pool_liquidity_smu.pdf?la=en);
[Cash Payups for Mortgages with Specified Characteristics — Freddie Mac
FAQ](https://sf.freddiemac.com/faqs/cash-payups-for-mortgages-with-specified-characteristics-faq)

### 3.7 CMO / REMIC structuring
Reference: `reference/fixed_income/cmo_remic_structuring.md`
(conceptual — a full tranche cash-flow waterfall is materially bigger
than this repo's small-transparent-function style; see the page for why)
Notebook: `notebooks/fixed_income/33_tba_dollar_roll_and_structuring.ipynb`
Resources: [Collateralized Mortgage Obligations (CMOs) —
thisMatter.com](https://thismatter.com/money/bonds/types/collateralized-mortgage-obligations.htm);
[Investor's Guide to RMBS & CMOs —
SIFMA](https://www.53.com/content/dam/fifth-third/docs/legal/fts-sifma-investors-guide.pdf)

### 3.8 OAS (mortgage context)
Reference: `reference/fixed_income/oas.md` and `mbs_convexity.md` — read
"What's demonstrable here, and what isn't" in `mbs_convexity.md` closely;
it's the single clearest statement in this repo of the line between a
correct cash-flow-timing result (WAL shift) and a claim this repo does
*not* make (full negative-convexity price behavior).

---

## Tier 4 — Integration

### 4.1 Capstone: everything on one portfolio
Notebook: `notebooks/integration/30_capstone_portfolio_review.ipynb` —
absolute and active risk decomposition, bond-level DV01, a rates
scenario and a credit scenario, and Brinson attribution composed into
the one-page summary a PM would actually read. This is where rates,
credit, and (via the portfolio's risk decomposition) the rest of this
roadmap gets applied together rather than one concept at a time.

### 4.2 Test yourself
- `/pmexpert exam` — a multi-concept assessment ladder spanning rates,
  credit, and mortgages together (`tutors/assessment_tutor.md`)
- `/pmexpert scenario` — walk a real `use_cases/*` workflow using
  concepts you've already confirmed
- `/pmexpert status` — check progress against the full 70-concept
  curriculum at any point

---

## What this roadmap deliberately leaves conceptual, not coded

Consistent with this repo's "state why, don't fake it" discipline (see
[OVERVIEW.md](./OVERVIEW.md)'s "What's implemented vs. conceptual-only"):
full OAS/negative-convexity price behavior, credit rating migration
matrices, non-agency/ABS/CMBS tranche waterfalls, leveraged loan
floating-rate/discount-margin pricing, specified-pool pay-ups, and
CMO/REMIC tranche cash-flow waterfalls. Each has its own reference page
explaining exactly what additional machinery would be required — treat
those as interview-ready conceptual fluency, not gaps to feel bad about.
Everything else in Tiers 1–3 above is tested `src/pm` code you can run,
not just read about.
