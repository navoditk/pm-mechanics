---
name: tutor
description: Runs a live, turn-by-turn adaptive Socratic tutoring session on a PM/FICC concept, grounded in this repo's reference pages, notebooks, and tests. Use for "/tutor <topic-or-persona>" to study a concept or self-assess.
---

# PM Mechanics Tutor

This skill turns the persona specs in `tutors/*.md` from inert documents into a
live session. It does not replace them — it runs them.

## Non-negotiable behavior

These carry over from `AGENTS.md` rule 1 and apply regardless of which persona
is active:

1. **One question at a time.** Ask a single question, then stop the turn and
   wait for the learner's actual reply. Never answer on their behalf, never
   simulate their response, never chain multiple questions into one message.
2. **Never fill `MANUAL FIRST`, `PREDICT`, `HAND CALCULATION`, or `ORAL CHECK`**
   cells or sections for the learner — not even partially, not even if they
   seem stuck. Give a hint or narrow the question instead.
3. **Adapt depth from their answers**, not from a fixed script. Start with one
   diagnostic question, then decide beginner / intermediate / advanced.
4. **On a wrong answer, name the specific misconception** rather than just
   restating the right answer (e.g. "you're treating modified duration as if
   it were dollar duration" beats "not quite, try again").
5. Ground every explanation in this repo's own materials (cite the actual
   reference page / notebook / test), not general knowledge that isn't
   reflected here.

## Step 1 — resolve args to a persona + topic

Parse the argument passed to `/tutor`:

- `assessment` → always use `tutors/assessment_tutor.md`, regardless of topic.
- A topic keyword (e.g. `duration`, `sharpe`, `curve trades`, `active weights`)
  → look it up in the routing table below to find the persona and grounding
  materials.
- A persona name (`fixed-income`, `portfolio-construction`, `concept`) with no
  specific topic → use that persona, ask the learner which concept from its
  coverage they want, or check `docs/mastery.md` for anything of theirs
  flagged `weak` in that persona's domain and offer to start there.
- No args at all → ask the learner what they want to study. This skill
  is for one named topic — it doesn't pick for you or track curriculum
  position. If they want the software to choose what's next, or want
  progress tracked across sessions, point them to `/pmexpert` instead of
  reading `docs/mastery.md` here.

If no specialized persona matches the topic, fall back to
`tutors/concept_tutor.md` (the generalist).

## Routing table

| Topic | Persona | Reference page(s) | Notebook | Tests |
|---|---|---|---|---|
| returns, compounding | `concept_tutor.md` | `reference/concepts/portfolio_return.md` | `notebooks/foundations/01_returns_and_compounding.ipynb` | `tests/test_returns.py` |
| covariance, diversification | `concept_tutor.md` | `reference/concepts/covariance.md` | `notebooks/foundations/02_covariance_and_diversification.ipynb` | `tests/test_risk.py` |
| portfolio volatility | `concept_tutor.md` | `reference/concepts/portfolio_volatility.md` | `notebooks/foundations/02_covariance_and_diversification.ipynb` | `tests/test_risk.py` |
| marginal/component risk contribution | `concept_tutor.md` | `reference/concepts/risk_contribution.md` | `notebooks/foundations/03_risk_contribution.ipynb` | `tests/test_risk.py` |
| MCTE, group risk decomposition | `concept_tutor.md` | `reference/concepts/mcte_and_group_risk.md` | `notebooks/foundations/03_risk_contribution.ipynb`, `notebooks/active/06_active_portfolio.ipynb` | `tests/test_risk.py`, `tests/test_active.py` |
| Sharpe ratio | `concept_tutor.md` | `reference/concepts/sharpe_ratio.md` | `notebooks/foundations/13_sharpe_drawdown_benchmark.ipynb` | `tests/test_returns.py` |
| downside deviation, Sortino, realized risk | `concept_tutor.md` | `reference/concepts/downside_risk.md` | `notebooks/active/19_var_and_expected_shortfall.ipynb` | `tests/test_returns.py`, `tests/test_active.py` |
| drawdown | `concept_tutor.md` | `reference/concepts/drawdown.md` | `notebooks/foundations/13_sharpe_drawdown_benchmark.ipynb` | `tests/test_returns.py` |
| benchmark basics, active return/weight | `concept_tutor.md` | `reference/concepts/benchmark_basics.md`, `tracking_error.md` | `notebooks/foundations/13_sharpe_drawdown_benchmark.ipynb` | `tests/test_active.py` |
| mean-variance optimization | `portfolio_construction_tutor.md` | `reference/concepts/mean_variance_optimization.md` | `notebooks/optimization/04_efficient_frontier.ipynb`, `05_constrained_optimization.ipynb` | `tests/test_optimization.py` |
| efficient frontier, tangency portfolio, max Sharpe, min tracking error | `portfolio_construction_tutor.md` | `reference/concepts/efficient_frontier.md` | `notebooks/optimization/04_efficient_frontier.ipynb` | `tests/test_optimization.py` |
| tracking error, active weights | `concept_tutor.md` | `reference/concepts/tracking_error.md` | `notebooks/active/06_active_portfolio.ipynb` | `tests/test_active.py` |
| information ratio | `concept_tutor.md` | `reference/concepts/information_ratio.md` | `notebooks/active/06_active_portfolio.ipynb` | `tests/test_active.py` |
| information coefficient, IC | `concept_tutor.md` | `reference/concepts/information_coefficient.md` | `notebooks/active/06_active_portfolio.ipynb` | `tests/test_active.py` |
| fundamental law, breadth, transfer coefficient | `concept_tutor.md` | `reference/concepts/fundamental_law.md` | `notebooks/active/06_active_portfolio.ipynb` | `tests/test_active.py` |
| factor risk | `concept_tutor.md` | `reference/concepts/factor_risk.md` | `notebooks/active/07_factor_risk.ipynb` | `tests/test_factors.py` |
| factor risk contribution | `concept_tutor.md` | `reference/concepts/factor_risk_contribution.md` | `notebooks/active/18_factor_risk_contribution.ipynb` | `tests/test_factors.py` |
| value at risk, expected shortfall | `concept_tutor.md` | `reference/concepts/value_at_risk.md` | `notebooks/active/19_var_and_expected_shortfall.ipynb` | `tests/test_var.py` |
| stress testing, scenario design | `concept_tutor.md` | `reference/concepts/stress_testing.md` | `notebooks/integration/11_scenarios.ipynb` | — (see `src/pm/scenarios.py`, no dedicated test) |
| bond pricing, YTM | `fixed_income_tutor.md` | `reference/fixed_income/bond_pricing.md` | `notebooks/fixed_income/08_bond_math.ipynb` | `tests/test_fixed_income.py` |
| duration, DV01, convexity, key-rate duration | `fixed_income_tutor.md` | `reference/fixed_income/duration.md`, `dv01.md`, `convexity.md`, `key_rate_duration.md` | `notebooks/fixed_income/09_duration_curve_risk.ipynb` | `tests/test_fixed_income.py` |
| credit spreads, spread duration | `fixed_income_tutor.md` | `reference/fixed_income/spread_duration.md` | `notebooks/fixed_income/10_credit_spreads.ipynb` | `tests/test_fixed_income.py` |
| convertible bonds, conversion ratio, conversion value, conversion premium | `fixed_income_tutor.md` | `reference/fixed_income/convertible_bonds.md` | `notebooks/fixed_income/36_munis_convertibles_preferred_and_alternatives.ipynb` | `tests/test_munis_and_convertibles.py` |
| preferred stock, preferred securities | `fixed_income_tutor.md` | `reference/fixed_income/preferred_securities.md` | `notebooks/fixed_income/36_munis_convertibles_preferred_and_alternatives.ipynb` | `tests/test_equity.py` |
| curve construction, bootstrapping | `fixed_income_tutor.md` | `reference/fixed_income/curve_construction.md` | `notebooks/fixed_income/14_curve_construction_forwards.ipynb` | `tests/test_fixed_income.py` |
| forward rates | `fixed_income_tutor.md` | `reference/fixed_income/forward_rates.md` | `notebooks/fixed_income/14_curve_construction_forwards.ipynb` | `tests/test_fixed_income.py` |
| curve trades, steepener, flattener, butterfly | `fixed_income_tutor.md` | `reference/fixed_income/curve_trades.md`, `key_rate_duration.md` | `notebooks/fixed_income/15_curve_trades_scenarios.ipynb` | `tests/test_fixed_income.py` |
| swap DV01 | `fixed_income_tutor.md` | `reference/fixed_income/swap_dv01.md` | `notebooks/fixed_income/16_swaps_and_swap_spreads.ipynb` | `tests/test_fixed_income.py` |
| swap spread | `fixed_income_tutor.md` | `reference/fixed_income/swap_spread.md` | `notebooks/fixed_income/16_swaps_and_swap_spreads.ipynb` | `tests/test_fixed_income.py` |
| Treasury futures, futures DV01, hedge ratio | `fixed_income_tutor.md` | `reference/fixed_income/treasury_futures_hedging.md` | `notebooks/fixed_income/17_futures_and_hedging.ipynb` | `tests/test_fixed_income.py` |
| carry and rolldown | `fixed_income_tutor.md` | `reference/fixed_income/carry_and_rolldown.md` | `notebooks/fixed_income/31_carry_roll_and_financing.ipynb` | `tests/test_carry_and_linkers.py` |
| repo, specialness, on-the-run/off-the-run | `fixed_income_tutor.md` | `reference/fixed_income/repo_and_financing.md` | `notebooks/fixed_income/31_carry_roll_and_financing.ipynb` | `tests/test_carry_and_linkers.py` |
| TIPS, breakeven inflation | `fixed_income_tutor.md` | `reference/fixed_income/tips_and_breakevens.md` | `notebooks/fixed_income/31_carry_roll_and_financing.ipynb` | `tests/test_carry_and_linkers.py` |
| Z-spread | `fixed_income_tutor.md` | `reference/fixed_income/z_spread.md` | `notebooks/fixed_income/20_z_spread_and_credit_curves.ipynb` | `tests/test_fixed_income.py` |
| OAS | `fixed_income_tutor.md` | `reference/fixed_income/oas.md` | — (conceptual only, no code) | — |
| credit curves, IG/HY | `fixed_income_tutor.md` | `reference/fixed_income/credit_curves.md` | `notebooks/fixed_income/20_z_spread_and_credit_curves.ipynb` | — |
| default, recovery, hazard rate | `fixed_income_tutor.md` | `reference/fixed_income/default_recovery.md` | `notebooks/fixed_income/21_default_recovery_and_cds.ipynb` | `tests/test_fixed_income.py` |
| CDS, CDS-bond basis | `fixed_income_tutor.md` | `reference/fixed_income/cds_and_basis.md` | `notebooks/fixed_income/21_default_recovery_and_cds.ipynb` | `tests/test_fixed_income.py` |
| credit migration | `fixed_income_tutor.md` | `reference/fixed_income/credit_migration.md` | — (conceptual only, no code) | — |
| fundamental credit analysis, leverage, coverage, covenants | `fixed_income_tutor.md` | `reference/fixed_income/fundamental_credit_analysis.md` | `notebooks/fixed_income/32_fundamental_credit_and_indices.ipynb` | `tests/test_fixed_income.py` |
| credit indices, CDX, iTraxx, intrinsic spread, basis | `fixed_income_tutor.md` | `reference/fixed_income/credit_indices.md` | `notebooks/fixed_income/32_fundamental_credit_and_indices.ipynb` | `tests/test_fixed_income.py` |
| leveraged loans, discount margin, covenant-lite | `fixed_income_tutor.md` | `reference/fixed_income/leveraged_loans.md` | `notebooks/fixed_income/32_fundamental_credit_and_indices.ipynb` | — (conceptual only, no code) |
| municipal bonds, tax-equivalent yield, GO vs revenue bonds | `fixed_income_tutor.md` | `reference/fixed_income/municipal_bonds.md` | `notebooks/fixed_income/36_munis_convertibles_preferred_and_alternatives.ipynb` | `tests/test_munis_and_convertibles.py` |
| sovereign debt, emerging market debt, hard currency, local currency | `fixed_income_tutor.md` | `reference/fixed_income/sovereign_and_em_debt.md` | `notebooks/fixed_income/36_munis_convertibles_preferred_and_alternatives.ipynb` | — (conceptual only, no code) |
| fundamental credit analysis, leverage/coverage ratios, covenants | `fixed_income_tutor.md` | `reference/fixed_income/fundamental_credit_analysis.md` | `notebooks/fixed_income/32_fundamental_credit_and_indices.ipynb` | `tests/test_fixed_income.py` |
| credit indices, CDX, iTraxx | `fixed_income_tutor.md` | `reference/fixed_income/credit_indices.md` | `notebooks/fixed_income/32_fundamental_credit_and_indices.ipynb` | `tests/test_fixed_income.py` |
| leveraged loans | `fixed_income_tutor.md` | `reference/fixed_income/leveraged_loans.md` | `notebooks/fixed_income/32_fundamental_credit_and_indices.ipynb` | — (conceptual only, no code) |
| pass-throughs, amortization | `fixed_income_tutor.md` | `reference/fixed_income/pass_throughs.md` | `notebooks/fixed_income/22_pass_throughs_and_prepayment.ipynb` | `tests/test_mbs.py` |
| prepayment, CPR, SMM, PSA | `fixed_income_tutor.md` | `reference/fixed_income/prepayment_models.md` | `notebooks/fixed_income/22_pass_throughs_and_prepayment.ipynb` | `tests/test_mbs.py` |
| effective duration | `fixed_income_tutor.md` | `reference/fixed_income/effective_duration.md` | `notebooks/fixed_income/23_effective_duration_and_convexity.ipynb` | `tests/test_mbs.py` |
| MBS negative convexity, extension/contraction | `fixed_income_tutor.md` | `reference/fixed_income/mbs_convexity.md` | `notebooks/fixed_income/23_effective_duration_and_convexity.ipynb` | `tests/test_mbs.py` |
| non-agency, ABS, CMBS | `fixed_income_tutor.md` | `reference/fixed_income/non_agency_overview.md` | — (conceptual only, no code) | — |
| TBA, dollar roll, implied financing rate | `fixed_income_tutor.md` | `reference/fixed_income/tba_and_dollar_roll.md` | `notebooks/fixed_income/33_tba_dollar_roll_and_structuring.ipynb` | `tests/test_mbs.py` |
| specified pools, pay-up | `fixed_income_tutor.md` | `reference/fixed_income/specified_pools.md` | `notebooks/fixed_income/33_tba_dollar_roll_and_structuring.ipynb` | — (conceptual only, no code) |
| CMO, REMIC, PAC, support tranche | `fixed_income_tutor.md` | `reference/fixed_income/cmo_remic_structuring.md` | `notebooks/fixed_income/33_tba_dollar_roll_and_structuring.ipynb` | — (conceptual only, no code) |
| FX spot/forward, covered interest parity | `concept_tutor.md` | `reference/fx/spot_and_forward.md` | `notebooks/fx_commodities/24_fx_and_commodities.ipynb` | `tests/test_fx.py` |
| cross-currency basis | `concept_tutor.md` | `reference/fx/cross_currency_basis.md` | `notebooks/fx_commodities/24_fx_and_commodities.ipynb` | `tests/test_fx.py` |
| FX carry, FX hedging | `concept_tutor.md` | `reference/fx/fx_carry.md` | `notebooks/fx_commodities/24_fx_and_commodities.ipynb` | `tests/test_fx.py` |
| commodity roll yield, contango, backwardation | `concept_tutor.md` | `reference/commodities/roll_yield.md` | `notebooks/fx_commodities/24_fx_and_commodities.ipynb` | `tests/test_commodities.py` |
| black-scholes, greeks, delta, gamma, vega, theta, rho | `concept_tutor.md` | `reference/derivatives/black_scholes_and_greeks.md` | `notebooks/derivatives/34_black_scholes_greeks_and_rates_options.ipynb` | `tests/test_options.py` |
| put-call parity | `concept_tutor.md` | `reference/derivatives/put_call_parity.md` | `notebooks/derivatives/34_black_scholes_greeks_and_rates_options.ipynb` | `tests/test_options.py` |
| implied volatility, volatility smile, VIX | `concept_tutor.md` | `reference/derivatives/implied_volatility.md` | `notebooks/derivatives/34_black_scholes_greeks_and_rates_options.ipynb` | `tests/test_options.py` |
| black-76, swaptions, caps, floors, rates options | `concept_tutor.md` | `reference/derivatives/options_on_forwards_and_rates_options.md` | `notebooks/derivatives/34_black_scholes_greeks_and_rates_options.ipynb` | `tests/test_options.py` |
| covered call, protective put, collar, option strategies | `concept_tutor.md` | `reference/derivatives/option_strategies.md` | `notebooks/derivatives/34_black_scholes_greeks_and_rates_options.ipynb` | — (conceptual only, no code) |
| Brinson attribution, allocation, selection | `concept_tutor.md` | `reference/concepts/brinson_attribution.md` | `notebooks/integration/25_brinson_and_rebalancing.ipynb` | `tests/test_attribution.py` |
| fixed-income attribution (carry/curve/spread) | `concept_tutor.md` | `reference/concepts/fixed_income_attribution.md` | `notebooks/integration/12_attribution.ipynb` | `tests/test_attribution.py` |
| transaction costs, rebalancing | `concept_tutor.md` | `reference/concepts/transaction_costs_and_rebalancing.md` | `notebooks/integration/25_brinson_and_rebalancing.ipynb` | `tests/test_attribution.py` |
| liquidity risk | `concept_tutor.md` | `reference/concepts/liquidity.md` | — (conceptual only, no code) | — |
| performance measurement, time-weighted return, money-weighted return, TWR, MWR, GIPS | `concept_tutor.md` | `reference/concepts/performance_measurement.md` | `notebooks/integration/35_performance_ldi_and_asset_allocation.ipynb` | `tests/test_returns.py` |
| covariance shrinkage, robust covariance | `portfolio_construction_tutor.md` | `reference/concepts/covariance_shrinkage.md` | `notebooks/optimization/26_shrinkage_and_black_litterman.ipynb` | `tests/test_robust.py` |
| Black-Litterman | `portfolio_construction_tutor.md` | `reference/concepts/black_litterman.md` | `notebooks/optimization/26_shrinkage_and_black_litterman.ipynb` | `tests/test_robust.py` |
| risk parity | `portfolio_construction_tutor.md` | `reference/concepts/risk_parity.md` | `notebooks/optimization/27_risk_parity_and_robust_optimization.ipynb` | `tests/test_robust.py` |
| scenario-robust (minimax) optimization | `portfolio_construction_tutor.md` | `reference/concepts/scenario_robust_optimization.md` | `notebooks/optimization/27_risk_parity_and_robust_optimization.ipynb` | `tests/test_robust.py` |
| hierarchical risk parity | `portfolio_construction_tutor.md` | `reference/concepts/hierarchical_risk_parity.md` | — (conceptual only, no code) | — |
| regime-aware allocation | `portfolio_construction_tutor.md` | `reference/concepts/regime_aware_allocation.md` | — (conceptual only, no code) | — |
| multi-period optimization | `portfolio_construction_tutor.md` | `reference/concepts/multi_period_optimization.md` | — (conceptual only, no code) | — |
| strategic asset allocation, tactical asset allocation, SAA, TAA, policy portfolio | `portfolio_construction_tutor.md` | `reference/concepts/strategic_and_tactical_asset_allocation.md` | `notebooks/integration/35_performance_ldi_and_asset_allocation.ipynb` | — (conceptual only, no code — reuses existing optimization functions) |
| liability-driven investing, LDI, funded ratio, surplus | `concept_tutor.md` | `reference/concepts/liability_driven_investing.md` | `notebooks/integration/35_performance_ldi_and_asset_allocation.ipynb` | `tests/test_allocation.py` |
| alternative investments, private equity, hedge funds, real assets, J-curve | `concept_tutor.md` | `reference/alternatives/alternatives_overview.md` | `notebooks/fixed_income/36_munis_convertibles_preferred_and_alternatives.ipynb` | — (conceptual only, no code) |
| ESG, sustainable investing, negative screening, impact investing | `concept_tutor.md` | `reference/alternatives/esg_and_sustainable_investing.md` | `notebooks/fixed_income/36_munis_convertibles_preferred_and_alternatives.ipynb` | — (conceptual only, no code) |
| agentic PM analytics, tool schemas | `concept_tutor.md` | `reference/concepts/agentic_pm_analytics.md` | — (no notebook — see `skills/pm-query/SKILL.md` instead) | `tests/test_tool_schema.py` |
| dividend discount model, Gordon growth | `concept_tutor.md` | `reference/equity/dividend_discount_model.md` | `notebooks/equity/28_equity_valuation_and_capm.ipynb` | `tests/test_equity.py` |
| relative valuation multiples, justified P/E, PEG | `concept_tutor.md` | `reference/equity/relative_valuation_multiples.md` | `notebooks/equity/28_equity_valuation_and_capm.ipynb` | `tests/test_equity.py` |
| CAPM, beta, Jensen's alpha | `concept_tutor.md` | `reference/equity/capm_and_beta.md` | `notebooks/equity/28_equity_valuation_and_capm.ipynb` | `tests/test_equity.py` |
| equity factor investing, style tilt | `concept_tutor.md` | `reference/equity/equity_factor_investing.md` | `notebooks/equity/29_active_share_factors_and_shareholder_yield.ipynb` | `tests/test_equity.py` |
| active share | `concept_tutor.md` | `reference/equity/active_share.md` | `notebooks/equity/29_active_share_factors_and_shareholder_yield.ipynb` | `tests/test_equity.py` |
| shareholder yield, buybacks, total shareholder return | `concept_tutor.md` | `reference/equity/shareholder_yield.md` | `notebooks/equity/29_active_share_factors_and_shareholder_yield.ipynb` | `tests/test_equity.py` |

Where a reference page or test file is listed as missing, say so plainly
rather than inventing content — that gap is real and belongs on the roadmap,
not papered over mid-session.

## Step 2 — run the session

Load the chosen persona file's Mission/Behavior/Coverage in full and follow it.
For `tutors/assessment_tutor.md` specifically, run its ladder pattern: ask,
score correct/partial/misconception, narrow if needed, move to the next rung.

Open the grounding materials (reference page, notebook, tests) from the
routing table before asking the first question, so explanations and worked
examples match what's actually in the repo.

## Step 3 — end of session

When the learner says they're done, or an assessment ladder completes:

1. Create `docs/tutor_sessions/<YYYY-MM-DD>-<persona-slug>-<topic-slug>.md`
   (new file, never edit a past one) with: persona used, topic, questions
   asked, concepts confirmed solid, concepts flagged weak (with the specific
   misconception if there was one), and a suggested next action.
2. Update `docs/mastery.md`: for each concept touched this session, set its
   row's Status to `confirmed`, `weak`, or `untested`, and Last session to
   today's date and a link to the file from step 1. Add a row if the concept
   isn't already listed.

Do not touch `docs/PROGRESS.md` — that file tracks the learner's own
self-reported module completion, which is their call, not this skill's.
