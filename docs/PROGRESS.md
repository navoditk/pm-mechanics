# Progress

## Current stage
The PM/FICC foundation is in place, extended one phase beyond FICC into equity portfolio management (Phase 13), and Phase 3 (active management) is now fully built out - it previously had only active weights and tracking error despite a reference page describing information ratio, IC, breadth, and the Fundamental Law as if they existed. A correctness-fix pass also closed several bugs a detailed audit surfaced (Black-Litterman round-trip, NaN propagation, silent optimizer failures, MBS domain errors), each with a regression test. That same audit's remaining findings are now closed too: the optimizer can trace an efficient frontier and find the tangency/min-TE portfolios (previously promised by a notebook title and never implemented), ex-post risk analytics (realized volatility/tracking error, downside deviation, MCTE/CCTE, group risk decomposition) fill the gap where everything used to be ex-ante only, and a pedagogy review's findings (thin early notebooks, zero plots, zero self-checks, a Day-0-shaped hole for true beginners, a stub capstone) are addressed: notebooks 02/03/05/07/11/12 rebuilt with self-checks and plots, a new Day 0 orientation notebook, `reference/glossary.md`, and a real capstone notebook using the three data CSVs no other notebook touched.

## Current health
- Test status: passing
- Last validated: `pytest -q`
- Result: `198 passed`
- Notebooks: 37, all valid JSON (`python scripts/check_repo.py`)

## Completed: rates/credit/mortgages PM-practitioner layer + roadmap
A user-requested audit found the fixed-income coverage strong on pricing
and risk mechanics but missing the practitioner/market-structure layer:
carry-and-rolldown was a broken ROADMAP Phase 5 promise, and TBA/dollar
roll, repo specialness, TIPS breakevens, credit indices, and fundamental
credit analysis had zero coverage. All three legs are done: rates
(carry/rolldown, repo and financing, TIPS/breakevens), credit
(fundamental credit analysis/leverage-coverage ratios, credit
indices/CDX-iTraxx, leveraged loans), and mortgages (TBA/dollar roll
implied financing rate, specified pools, CMO/REMIC structuring) - each
with code (where genuinely codeable), reference pages, notebooks, and
verified external sources, all wired in. Also caught and fixed
mid-mortgages-work: the Credit PR had shipped its three new reference
pages without adding matching rows to `docs/mastery.md` or the `/tutor`
routing table - fixed there, and `/pmexpert`'s confirmed-count level table
(stale at "all 55" since before the Rates PR) updated to the true total
of 70 concepts. Closing the loop:
`docs/rates_credit_mortgages_roadmap.md` sequences the full path (bond
pricing through TBA/dollar roll and CMO/REMIC structuring) with a
reference page, notebook, and verified resource at every step - the
user's original ask that started this whole workstream.

## Completed: curriculum-completeness audit
A repo-wide audit (not scoped to fixed income this time) found the
curriculum strong across portfolio theory, risk, and every FICC/equity
topic built so far, but with real gaps from a PM perspective: zero
options/volatility coverage anywhere, no asset-allocation framing
(SAA/TAA, liability-driven investing) on top of the existing optimization
machinery, no performance-measurement fundamentals (time-weighted vs.
money-weighted return, GIPS), and narrower gaps in munis, sovereign/EM
debt, convertibles, preferred securities, alternatives/private markets,
ESG, and `use_cases/` coverage. All four planned workstreams are done:
glossary backfill, options and volatility (Phase 14: Black-Scholes, all
five Greeks each cross-checked against a finite-difference bump, implied
volatility, Black-76), asset allocation/performance measurement (Phase
15: `money_weighted_return` verified against the classic TWR-vs-MWR
divergence case; `funded_ratio`/`surplus` for LDI, reusing existing
`dv01`/`hedge_ratio`), and the wider investable universe (Phase 16:
municipal bonds `tax_equivalent_yield`, convertible bonds
`conversion_value`/`conversion_premium`, preferred securities reusing
`gordon_growth_value` at zero growth with no new function needed;
sovereign/EM debt, alternatives, and ESG conceptual; plus 4 new use
cases - FX hedge, commodity futures roll, MBS extension scenario,
fundamental credit review - closing every gap `use_cases/index.md`'s
"Future" list had named).

## Completed modules
- Foundations bootcamp structure in place
- Core PM analytics library implemented under `src/pm/`
- Fixed-income, optimization, integration, FX/commodities, equity, and active-management notebooks present
- Reference pages added across portfolio foundations, optimization, risk, FICC, equity, and active management (information ratio, information coefficient, Fundamental Law, efficient frontier, downside risk, MCTE/group risk) - each with real external sources
- `docs/OVERVIEW.md` added as a quick-read repo summary
- `/pmexpert` rebuilt as a single self-contained trainer (lesson/quiz/scenario/exam/status modes) with `docs/mastery-guide.md` as its walkthrough
- Correctness-fix pass on `src/pm` (Black-Litterman round-trip, NaN propagation, silent solver failures, MBS domain errors)
- Efficient frontier / tangency portfolio / min-tracking-error optimizers added; notebook 04 now actually plots a frontier (previously titled but empty)
- Ex-post risk analytics added (realized volatility/tracking error, downside deviation, MCTE/CCTE, group risk decomposition); notebook 19 now plots the VaR/ES tail and checks a risk model's assumption against realized data
- Zero-to-proficiency pedagogy pass: notebooks 02/03/05/07/11/12 rebuilt (self-check asserts, plots, PREDICT before code); `notebooks/foundations/00_orientation.ipynb` added for true beginners (environment check, learning-cycle explainer, `w'Sigma*w` by hand); `reference/glossary.md` added (49 terms, every link verified); `notebooks/integration/30_capstone_portfolio_review.ipynb` added, the repo's first real capstone, using `data/mock_portfolio.csv`, `mock_benchmark.csv`, and `mock_bonds.csv` for the first time
- Rates PM-practitioner layer: `carry_and_rolldown.md`/`repo_and_financing.md`/`tips_and_breakevens.md` (each tested `src/pm` code + real external sources), notebook 31, closing the broken "carry and roll" ROADMAP Phase 5 promise
- Credit PM-practitioner layer: `fundamental_credit_analysis.md`/`credit_indices.md`/`leveraged_loans.md` (leverage/coverage ratios and CDX/iTraxx intrinsic-value/basis are tested `src/pm` code; leveraged loans and covenant/rating-agency mechanics are conceptual-only, same honesty pattern as OAS), notebook 32
- Mortgages PM-practitioner layer: `tba_and_dollar_roll.md` (tested `src/pm` code - `dollar_roll_implied_financing_rate`, verified against a real published worked example), `specified_pools.md` and `cmo_remic_structuring.md` (conceptual-only, same honesty pattern as OAS/leveraged loans), notebook 33 - closes the rates/credit/mortgages PM-practitioner-layer audit entirely
- `docs/rates_credit_mortgages_roadmap.md` added: a single sequenced zero-to-hero path across all of rates, credit, and mortgages, every step linking its reference page, notebook, and a verified external resource - wired into `docs/README.md`, `docs/learning-paths.md`, `docs/OVERVIEW.md`, root `README.md`, and `mkdocs.yml` nav
- `reference/glossary.md` backfilled: 12 new Fixed Income terms (carry, rolldown, repo/specialness, on-the-run/off-the-run, TIPS/breakevens, leverage/coverage ratios, credit indices, leveraged loans, TBA/dollar roll, specified pools, CMO/REMIC) plus new FX and Commodities sections that didn't exist before, despite both asset classes already having real reference-page content - all 64 links verified to resolve
- Phase 14 (derivatives and options) built: `src/pm/options.py` (Black-Scholes call/put pricing, delta/gamma/vega/theta/rho, implied volatility via `brentq`, Black-76) - every Greek independently verified against a finite-difference bump of the pricing function itself, not just the closed-form formula, and Black-76 verified to reproduce Black-Scholes exactly at the matching forward price; 5 new reference pages (`black_scholes_and_greeks.md`, `put_call_parity.md`, `implied_volatility.md`, `options_on_forwards_and_rates_options.md`, `option_strategies.md` - the last two conceptual for the curve/annuity layer and strategy-composition reasons stated on each page) and notebook 34, closing this repo's single largest coverage gap found by the completeness audit
- Phase 15 (asset allocation and performance measurement) built: `pm.returns.money_weighted_return` (solved via `brentq`, verified against the classic CFA textbook TWR-vs-MWR divergence case - a flat 0% time-weighted return alongside a roughly -26.8% money-weighted return) and `pm.allocation.funded_ratio`/`surplus` for liability-driven investing (reusing existing `dv01`/`hedge_ratio` for duration matching rather than new formulas); 3 new reference pages (`performance_measurement.md`, `liability_driven_investing.md`, `strategic_and_tactical_asset_allocation.md` - the last two conceptual, since SAA/TAA reapplies existing optimization tools and GIPS composite construction is a compliance layer on top of the existing `cumulative_return`) and notebook 35, closing the completeness audit's second-largest gap
- Phase 16 (wider investable universe) built: `pm.fixed_income.munis.tax_equivalent_yield`, `pm.fixed_income.convertibles.conversion_value`/`conversion_premium`, and a confirmation that preferred-stock valuation needs no new function at all (`gordon_growth_value` at `growth_rate=0` is exactly the perpetuity formula, verified in `tests/test_equity.py`); 4 new reference pages (`municipal_bonds.md`, `convertible_bonds.md`, `preferred_securities.md`, `sovereign_and_em_debt.md`) plus a new `reference/alternatives/` section (`alternatives_overview.md`, `esg_and_sustainable_investing.md`, both conceptual survey pages) and notebook 36; 4 new use cases (FX hedge, commodity futures roll, MBS extension scenario, fundamental credit review) close every item `use_cases/index.md`'s "Future" list had named except multi-asset risk-off and risk-budget breach - this closes the curriculum-completeness audit entirely

## In progress
- Documentation consolidation and onboarding cleanup
- Keeping the root README and docs hub aligned with the actual repo state
- Maintaining a clean learning-first workflow around each new concept

## Next recommended action
Open:
- `curriculum/bootcamp_01_foundations/README.md`
- `notebooks/foundations/01_returns_and_compounding.ipynb`

## Completion rule
Only mark a module complete when:
- the manual exercise has been attempted,
- the relevant tests pass,
- the reference page has been reviewed or updated,
- the concept can be explained in plain PM language.

## Branch / PR tracking

Current branch:
`feat/tier-b-c-gaps-munis-converts-preferred-em-alts-esg-usecases`

Current issue:
_Use issue/branch naming for each learning unit_

Current PR:
_None open — #1 (Phase 13 equity), #2 (correctness-fix pass), #3 (Phase 3 active management), #4 (efficient frontier/ex-post risk), #5 (zero-to-proficiency pedagogy), #6 (rates PM-practitioner layer), #7 (credit PM-practitioner layer), #8 (mortgages PM-practitioner layer), #9 (rates/credit/mortgages roadmap), #10 (glossary backfill), #11 (derivatives and options), and #12 (asset allocation and performance measurement) merged to `main`_

Last pushed checkpoint:
_Not pushed yet — local commits only_
