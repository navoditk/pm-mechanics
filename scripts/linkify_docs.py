"""Rewrite plain-text cross-references into real clickable markdown links
across reference/index.md, every reference page's "## Related" section,
curriculum/bootcamp_01_foundations/README.md's notebook lists, and
use_cases/index.md. Content doesn't change (same concepts, same notebooks)
- only backtick-only mentions become real [text](path) links, so GitHub,
the MkDocs site, and (via build_artifact_preview.py's link resolution)
the Artifact preview can all navigate them directly.

Run: python scripts/linkify_docs.py
Then rebuild both docs surfaces to verify: build_docs_site.py + mkdocs
build --strict, and build_artifact_preview.py.
"""
import os
import re
from pathlib import Path

from reference_taxonomy import NOTEBOOKS, SECTIONS, TITLES, USE_CASES

ROOT = Path(__file__).resolve().parents[1]
REF_ROOT = ROOT / "reference"

# path (relative to reference/) -> [(display text, target path relative to reference/)]
# Preserves each page's existing Related content, just as real links.
RELATED = {
    "commodities/roll_yield.md": [
        ("FX carry (the FX analogue)", "fx/fx_carry.md"),
        ("Forward rates", "fixed_income/forward_rates.md"),
    ],
    "concepts/backtesting_biases.md": [
        ("Performance measurement", "concepts/performance_measurement.md"),
        ("Information coefficient", "concepts/information_coefficient.md"),
        ("Liquidity", "concepts/liquidity.md"),
        ("Transaction costs and rebalancing", "concepts/transaction_costs_and_rebalancing.md"),
    ],
    "concepts/benchmark_basics.md": [
        ("Tracking error", "concepts/tracking_error.md"),
        ("Information ratio", "concepts/information_ratio.md"),
        ("Fundamental Law", "concepts/fundamental_law.md"),
    ],
    "concepts/black_litterman.md": [
        ("Covariance shrinkage", "concepts/covariance_shrinkage.md"),
        ("Mean-variance optimization", "concepts/mean_variance_optimization.md"),
        ("Risk parity", "concepts/risk_parity.md"),
    ],
    "concepts/brinson_attribution.md": [
        ("Tracking error", "concepts/tracking_error.md"),
        ("Benchmark basics (active weights)", "concepts/benchmark_basics.md"),
        ("Fixed-income attribution", "concepts/fixed_income_attribution.md"),
    ],
    "concepts/covariance_shrinkage.md": [
        ("Mean-variance optimization", "concepts/mean_variance_optimization.md"),
        ("Black-Litterman", "concepts/black_litterman.md"),
        ("Risk parity", "concepts/risk_parity.md"),
    ],
    "concepts/covariance.md": [
        ("Portfolio volatility", "concepts/portfolio_volatility.md"),
        ("Risk contribution", "concepts/risk_contribution.md"),
    ],
    "concepts/drawdown.md": [
        ("Sharpe ratio", "concepts/sharpe_ratio.md"),
        ("Portfolio volatility", "concepts/portfolio_volatility.md"),
    ],
    "concepts/factor_risk_contribution.md": [
        ("Factor risk", "concepts/factor_risk.md"),
        ("Risk contribution", "concepts/risk_contribution.md"),
        ("Tracking error", "concepts/tracking_error.md"),
    ],
    "concepts/factor_risk.md": [
        ("Tracking error", "concepts/tracking_error.md"),
        ("Risk contribution", "concepts/risk_contribution.md"),
        ("Factor risk contribution", "concepts/factor_risk_contribution.md"),
        ("Mean-variance optimization", "concepts/mean_variance_optimization.md"),
    ],
    "concepts/fixed_income_attribution.md": [
        ("Brinson attribution", "concepts/brinson_attribution.md"),
        ("Key-rate duration", "fixed_income/key_rate_duration.md"),
        ("Spread duration", "fixed_income/spread_duration.md"),
    ],
    "concepts/hierarchical_risk_parity.md": [
        ("Risk parity", "concepts/risk_parity.md"),
        ("Covariance shrinkage", "concepts/covariance_shrinkage.md"),
    ],
    "concepts/liquidity.md": [
        ("Transaction costs and rebalancing", "concepts/transaction_costs_and_rebalancing.md"),
        ("Stress testing", "concepts/stress_testing.md"),
    ],
    "concepts/liability_driven_investing.md": [
        ("Duration, DV01", "fixed_income/duration.md"),
        ("Performance measurement", "concepts/performance_measurement.md"),
        ("Strategic and tactical asset allocation", "concepts/strategic_and_tactical_asset_allocation.md"),
    ],
    "concepts/mean_variance_optimization.md": [
        ("Efficient frontier and tangency portfolio", "concepts/efficient_frontier.md"),
        ("Covariance shrinkage", "concepts/covariance_shrinkage.md"),
        ("Risk parity", "concepts/risk_parity.md"),
        ("Transaction costs and rebalancing", "concepts/transaction_costs_and_rebalancing.md"),
    ],
    "concepts/efficient_frontier.md": [
        ("Mean-variance optimization", "concepts/mean_variance_optimization.md"),
        ("Black-Litterman", "concepts/black_litterman.md"),
        ("Sharpe ratio", "concepts/sharpe_ratio.md"),
    ],
    "concepts/multi_period_optimization.md": [
        ("Transaction costs and rebalancing", "concepts/transaction_costs_and_rebalancing.md"),
        ("Scenario-robust optimization", "concepts/scenario_robust_optimization.md"),
    ],
    "concepts/performance_measurement.md": [
        ("Sharpe ratio", "concepts/sharpe_ratio.md"),
        ("Brinson attribution", "concepts/brinson_attribution.md"),
        ("Backtesting biases", "concepts/backtesting_biases.md"),
        ("Liability-driven investing", "concepts/liability_driven_investing.md"),
    ],
    "concepts/portfolio_return.md": [
        ("Portfolio volatility", "concepts/portfolio_volatility.md"),
        ("Sharpe ratio", "concepts/sharpe_ratio.md"),
    ],
    "concepts/portfolio_volatility.md": [
        ("Covariance", "concepts/covariance.md"),
        ("Risk contribution", "concepts/risk_contribution.md"),
    ],
    "concepts/regime_aware_allocation.md": [
        ("Covariance shrinkage", "concepts/covariance_shrinkage.md"),
        ("Stress testing", "concepts/stress_testing.md"),
        ("Scenario-robust optimization", "concepts/scenario_robust_optimization.md"),
    ],
    "concepts/risk_contribution.md": [
        ("Portfolio volatility", "concepts/portfolio_volatility.md"),
        ("Factor risk contribution", "concepts/factor_risk_contribution.md"),
        ("MCTE and group risk decomposition", "concepts/mcte_and_group_risk.md"),
    ],
    "concepts/mcte_and_group_risk.md": [
        ("Risk contribution", "concepts/risk_contribution.md"),
        ("Tracking error", "concepts/tracking_error.md"),
        ("Factor risk contribution", "concepts/factor_risk_contribution.md"),
    ],
    "concepts/risk_parity.md": [
        ("Risk contribution", "concepts/risk_contribution.md"),
        ("Mean-variance optimization", "concepts/mean_variance_optimization.md"),
        ("Covariance shrinkage", "concepts/covariance_shrinkage.md"),
    ],
    "concepts/scenario_robust_optimization.md": [
        ("Stress testing", "concepts/stress_testing.md"),
        ("Mean-variance optimization", "concepts/mean_variance_optimization.md"),
        ("Black-Litterman", "concepts/black_litterman.md"),
    ],
    "concepts/sharpe_ratio.md": [
        ("Portfolio volatility", "concepts/portfolio_volatility.md"),
        ("Drawdown", "concepts/drawdown.md"),
        ("Downside deviation and realized risk", "concepts/downside_risk.md"),
    ],
    "concepts/strategic_and_tactical_asset_allocation.md": [
        ("Mean-variance optimization", "concepts/mean_variance_optimization.md"),
        ("Efficient frontier and tangency portfolio", "concepts/efficient_frontier.md"),
        ("Black-Litterman", "concepts/black_litterman.md"),
        ("Risk parity", "concepts/risk_parity.md"),
        ("Liability-driven investing", "concepts/liability_driven_investing.md"),
    ],
    "concepts/downside_risk.md": [
        ("Information ratio", "concepts/information_ratio.md"),
        ("Sharpe ratio", "concepts/sharpe_ratio.md"),
        ("Drawdown", "concepts/drawdown.md"),
        ("Value at risk", "concepts/value_at_risk.md"),
    ],
    "concepts/stress_testing.md": [
        ("Value at risk", "concepts/value_at_risk.md"),
        ("Key-rate duration", "fixed_income/key_rate_duration.md"),
        ("Backtesting biases", "concepts/backtesting_biases.md"),
    ],
    "concepts/tracking_error.md": [
        ("Benchmark basics", "concepts/benchmark_basics.md"),
        ("Information ratio", "concepts/information_ratio.md"),
        ("MCTE and group risk decomposition", "concepts/mcte_and_group_risk.md"),
        ("Brinson attribution", "concepts/brinson_attribution.md"),
        ("Factor risk", "concepts/factor_risk.md"),
    ],
    "concepts/information_ratio.md": [
        ("Tracking error", "concepts/tracking_error.md"),
        ("MCTE and group risk decomposition", "concepts/mcte_and_group_risk.md"),
        ("Downside deviation and realized risk", "concepts/downside_risk.md"),
        ("Fundamental Law", "concepts/fundamental_law.md"),
        ("Sharpe ratio", "concepts/sharpe_ratio.md"),
    ],
    "concepts/information_coefficient.md": [
        ("Fundamental Law", "concepts/fundamental_law.md"),
        ("Information ratio", "concepts/information_ratio.md"),
    ],
    "concepts/fundamental_law.md": [
        ("Information coefficient", "concepts/information_coefficient.md"),
        ("Information ratio", "concepts/information_ratio.md"),
        ("Active share", "equity/active_share.md"),
    ],
    "concepts/transaction_costs_and_rebalancing.md": [
        ("Liquidity", "concepts/liquidity.md"),
        ("Mean-variance optimization (constraints)", "concepts/mean_variance_optimization.md"),
        ("Brinson attribution", "concepts/brinson_attribution.md"),
    ],
    "concepts/value_at_risk.md": [
        ("Portfolio volatility", "concepts/portfolio_volatility.md"),
        ("Stress testing", "concepts/stress_testing.md"),
    ],
    "equity/active_share.md": [
        ("Tracking error", "concepts/tracking_error.md"),
        ("Equity factor investing (style tilt)", "equity/equity_factor_investing.md"),
    ],
    "equity/capm_and_beta.md": [
        ("Dividend discount model", "equity/dividend_discount_model.md"),
        ("Equity factor investing", "equity/equity_factor_investing.md"),
        ("Factor risk", "concepts/factor_risk.md"),
    ],
    "equity/dividend_discount_model.md": [
        ("Relative valuation multiples", "equity/relative_valuation_multiples.md"),
        ("CAPM and beta", "equity/capm_and_beta.md"),
        ("Shareholder yield", "equity/shareholder_yield.md"),
        ("Preferred securities", "fixed_income/preferred_securities.md"),
    ],
    "equity/equity_factor_investing.md": [
        ("Active share", "equity/active_share.md"),
        ("CAPM and beta", "equity/capm_and_beta.md"),
        ("Factor risk", "concepts/factor_risk.md"),
        ("Factor risk contribution", "concepts/factor_risk_contribution.md"),
    ],
    "derivatives/black_scholes_and_greeks.md": [
        ("Put-call parity", "derivatives/put_call_parity.md"),
        ("Implied volatility", "derivatives/implied_volatility.md"),
        ("Options on forwards and rates options", "derivatives/options_on_forwards_and_rates_options.md"),
        ("Option strategies", "derivatives/option_strategies.md"),
    ],
    "derivatives/put_call_parity.md": [
        ("Black-Scholes pricing and the Greeks", "derivatives/black_scholes_and_greeks.md"),
        ("Implied volatility", "derivatives/implied_volatility.md"),
        ("Option strategies", "derivatives/option_strategies.md"),
    ],
    "derivatives/implied_volatility.md": [
        ("Black-Scholes pricing and the Greeks", "derivatives/black_scholes_and_greeks.md"),
        ("Put-call parity", "derivatives/put_call_parity.md"),
    ],
    "derivatives/options_on_forwards_and_rates_options.md": [
        ("Black-Scholes pricing and the Greeks", "derivatives/black_scholes_and_greeks.md"),
        ("Curve construction", "fixed_income/curve_construction.md"),
        ("Swap DV01", "fixed_income/swap_dv01.md"),
        ("MBS convexity", "fixed_income/mbs_convexity.md"),
    ],
    "derivatives/option_strategies.md": [
        ("Black-Scholes pricing and the Greeks", "derivatives/black_scholes_and_greeks.md"),
        ("Put-call parity", "derivatives/put_call_parity.md"),
        ("Equity factor investing", "equity/equity_factor_investing.md"),
    ],
    "equity/relative_valuation_multiples.md": [
        ("Dividend discount model", "equity/dividend_discount_model.md"),
        ("CAPM and beta", "equity/capm_and_beta.md"),
    ],
    "equity/shareholder_yield.md": [
        ("Dividend discount model", "equity/dividend_discount_model.md"),
        ("Relative valuation multiples", "equity/relative_valuation_multiples.md"),
    ],
    "fixed_income/accrued_interest_and_settlement.md": [
        ("Bond pricing", "fixed_income/bond_pricing.md"),
        ("Repo and financing", "fixed_income/repo_and_financing.md"),
        ("Carry and rolldown", "fixed_income/carry_and_rolldown.md"),
        ("Duration", "fixed_income/duration.md"),
    ],
    "fixed_income/bond_pricing.md": [
        ("Accrued interest and settlement", "fixed_income/accrued_interest_and_settlement.md"),
        ("Duration", "fixed_income/duration.md"),
        ("DV01", "fixed_income/dv01.md"),
        ("Curve construction", "fixed_income/curve_construction.md"),
        ("TIPS and breakeven inflation", "fixed_income/tips_and_breakevens.md"),
        ("Convertible bonds", "fixed_income/convertible_bonds.md"),
    ],
    "fixed_income/convertible_bonds.md": [
        ("Bond pricing", "fixed_income/bond_pricing.md"),
        ("Black-Scholes pricing and the Greeks", "derivatives/black_scholes_and_greeks.md"),
        ("Preferred securities", "fixed_income/preferred_securities.md"),
    ],
    "fixed_income/preferred_securities.md": [
        ("Convertible bonds", "fixed_income/convertible_bonds.md"),
        ("OAS", "fixed_income/oas.md"),
        ("Dividend discount model", "equity/dividend_discount_model.md"),
    ],
    "fixed_income/municipal_bonds.md": [
        ("Fundamental credit analysis", "fixed_income/fundamental_credit_analysis.md"),
        ("TIPS and breakeven inflation", "fixed_income/tips_and_breakevens.md"),
        ("Sovereign and EM debt", "fixed_income/sovereign_and_em_debt.md"),
    ],
    "fixed_income/sovereign_and_em_debt.md": [
        ("Credit curves", "fixed_income/credit_curves.md"),
        ("CDS and basis", "fixed_income/cds_and_basis.md"),
        ("FX carry", "fx/fx_carry.md"),
        ("Municipal bonds", "fixed_income/municipal_bonds.md"),
    ],
    "fixed_income/carry_and_rolldown.md": [
        ("Duration", "fixed_income/duration.md"),
        ("Curve trades", "fixed_income/curve_trades.md"),
        ("Repo and financing", "fixed_income/repo_and_financing.md"),
        ("Forward rates", "fixed_income/forward_rates.md"),
    ],
    "fixed_income/repo_and_financing.md": [
        ("Carry and rolldown", "fixed_income/carry_and_rolldown.md"),
        ("Curve trades", "fixed_income/curve_trades.md"),
        ("Treasury futures hedging", "fixed_income/treasury_futures_hedging.md"),
        ("TBA and the dollar roll", "fixed_income/tba_and_dollar_roll.md"),
    ],
    "fixed_income/tips_and_breakevens.md": [
        ("Bond pricing", "fixed_income/bond_pricing.md"),
        ("Forward rates", "fixed_income/forward_rates.md"),
        ("Carry and rolldown", "fixed_income/carry_and_rolldown.md"),
    ],
    "fixed_income/cds_and_basis.md": [
        ("Default and recovery", "fixed_income/default_recovery.md"),
        ("Z-spread", "fixed_income/z_spread.md"),
        ("Credit curves", "fixed_income/credit_curves.md"),
        ("Credit indices", "fixed_income/credit_indices.md"),
    ],
    "fixed_income/convexity.md": [
        ("Duration", "fixed_income/duration.md"),
        ("DV01", "fixed_income/dv01.md"),
        ("MBS negative convexity", "fixed_income/mbs_convexity.md"),
        ("Curve trades", "fixed_income/curve_trades.md"),
    ],
    "fixed_income/credit_curves.md": [
        ("Curve construction", "fixed_income/curve_construction.md"),
        ("Z-spread", "fixed_income/z_spread.md"),
        ("Default and recovery", "fixed_income/default_recovery.md"),
        ("Sovereign and EM debt", "fixed_income/sovereign_and_em_debt.md"),
    ],
    "fixed_income/credit_migration.md": [
        ("Default and recovery", "fixed_income/default_recovery.md"),
        ("Credit curves", "fixed_income/credit_curves.md"),
        ("Fundamental credit analysis", "fixed_income/fundamental_credit_analysis.md"),
        ("Stress testing (portfolio credit scenarios)", "concepts/stress_testing.md"),
    ],
    "fixed_income/fundamental_credit_analysis.md": [
        ("Spread duration", "fixed_income/spread_duration.md"),
        ("Default and recovery", "fixed_income/default_recovery.md"),
        ("Credit migration", "fixed_income/credit_migration.md"),
        ("Leveraged loans", "fixed_income/leveraged_loans.md"),
        ("Credit indices", "fixed_income/credit_indices.md"),
    ],
    "fixed_income/credit_indices.md": [
        ("Fundamental credit analysis", "fixed_income/fundamental_credit_analysis.md"),
        ("CDS and basis", "fixed_income/cds_and_basis.md"),
        ("Credit curves", "fixed_income/credit_curves.md"),
    ],
    "fixed_income/leveraged_loans.md": [
        ("Fundamental credit analysis", "fixed_income/fundamental_credit_analysis.md"),
        ("Spread duration", "fixed_income/spread_duration.md"),
        ("Credit curves", "fixed_income/credit_curves.md"),
        ("Alternative investments overview", "alternatives/alternatives_overview.md"),
    ],
    "fixed_income/curve_construction.md": [
        ("Forward rates", "fixed_income/forward_rates.md"),
        ("Key-rate duration", "fixed_income/key_rate_duration.md"),
        ("Curve trades", "fixed_income/curve_trades.md"),
    ],
    "fixed_income/curve_trades.md": [
        ("Key-rate duration", "fixed_income/key_rate_duration.md"),
        ("Forward rates", "fixed_income/forward_rates.md"),
        ("Carry and rolldown", "fixed_income/carry_and_rolldown.md"),
        ("Repo and financing", "fixed_income/repo_and_financing.md"),
        ("Stress testing (scenario analysis)", "concepts/stress_testing.md"),
    ],
    "fixed_income/default_recovery.md": [
        ("CDS and basis", "fixed_income/cds_and_basis.md"),
        ("Z-spread", "fixed_income/z_spread.md"),
        ("Credit curves", "fixed_income/credit_curves.md"),
    ],
    "fixed_income/duration.md": [
        ("DV01", "fixed_income/dv01.md"),
        ("Convexity", "fixed_income/convexity.md"),
        ("Key-rate duration", "fixed_income/key_rate_duration.md"),
        ("Effective duration", "fixed_income/effective_duration.md"),
        ("Carry and rolldown", "fixed_income/carry_and_rolldown.md"),
    ],
    "fixed_income/dv01.md": [
        ("Duration", "fixed_income/duration.md"),
        ("Convexity", "fixed_income/convexity.md"),
        ("Key-rate duration", "fixed_income/key_rate_duration.md"),
    ],
    "fixed_income/effective_duration.md": [
        ("Duration", "fixed_income/duration.md"),
        ("MBS negative convexity", "fixed_income/mbs_convexity.md"),
        ("Prepayment models", "fixed_income/prepayment_models.md"),
    ],
    "fixed_income/forward_rates.md": [
        ("Curve construction", "fixed_income/curve_construction.md"),
        ("Curve trades", "fixed_income/curve_trades.md"),
    ],
    "fixed_income/key_rate_duration.md": [
        ("DV01", "fixed_income/dv01.md"),
        ("Curve trades (steepener/flattener, butterfly)", "fixed_income/curve_trades.md"),
    ],
    "fixed_income/mbs_convexity.md": [
        ("Prepayment models", "fixed_income/prepayment_models.md"),
        ("Effective duration", "fixed_income/effective_duration.md"),
        ("OAS", "fixed_income/oas.md"),
        ("CMO/REMIC structuring", "fixed_income/cmo_remic_structuring.md"),
    ],
    "fixed_income/non_agency_overview.md": [
        ("Pass-throughs", "fixed_income/pass_throughs.md"),
        ("Credit curves", "fixed_income/credit_curves.md"),
        ("CDS and basis", "fixed_income/cds_and_basis.md"),
        ("CMO/REMIC structuring", "fixed_income/cmo_remic_structuring.md"),
    ],
    "fixed_income/oas.md": [
        ("Z-spread", "fixed_income/z_spread.md"),
        ("Effective duration", "fixed_income/effective_duration.md"),
    ],
    "fixed_income/pass_throughs.md": [
        ("Prepayment models", "fixed_income/prepayment_models.md"),
        ("Effective duration", "fixed_income/effective_duration.md"),
        ("TBA and the dollar roll", "fixed_income/tba_and_dollar_roll.md"),
        ("Specified pools", "fixed_income/specified_pools.md"),
    ],
    "fixed_income/tba_and_dollar_roll.md": [
        ("Repo and financing", "fixed_income/repo_and_financing.md"),
        ("Specified pools", "fixed_income/specified_pools.md"),
        ("Pass-throughs", "fixed_income/pass_throughs.md"),
        ("Prepayment models", "fixed_income/prepayment_models.md"),
    ],
    "fixed_income/specified_pools.md": [
        ("TBA and the dollar roll", "fixed_income/tba_and_dollar_roll.md"),
        ("Prepayment models", "fixed_income/prepayment_models.md"),
        ("MBS negative convexity", "fixed_income/mbs_convexity.md"),
        ("Pass-throughs", "fixed_income/pass_throughs.md"),
    ],
    "fixed_income/cmo_remic_structuring.md": [
        ("MBS negative convexity", "fixed_income/mbs_convexity.md"),
        ("Prepayment models", "fixed_income/prepayment_models.md"),
        ("Non-agency overview", "fixed_income/non_agency_overview.md"),
        ("Pass-throughs", "fixed_income/pass_throughs.md"),
    ],
    "fixed_income/prepayment_models.md": [
        ("Pass-throughs", "fixed_income/pass_throughs.md"),
        ("MBS negative convexity", "fixed_income/mbs_convexity.md"),
        ("Effective duration", "fixed_income/effective_duration.md"),
    ],
    "fixed_income/spread_duration.md": [
        ("Z-spread", "fixed_income/z_spread.md"),
        ("Credit curves", "fixed_income/credit_curves.md"),
        ("Fundamental credit analysis", "fixed_income/fundamental_credit_analysis.md"),
    ],
    "fixed_income/swap_dv01.md": [
        ("Swap spread", "fixed_income/swap_spread.md"),
        ("DV01", "fixed_income/dv01.md"),
    ],
    "fixed_income/swap_spread.md": [
        ("Swap DV01", "fixed_income/swap_dv01.md"),
        ("Curve construction", "fixed_income/curve_construction.md"),
    ],
    "fixed_income/treasury_futures_hedging.md": [
        ("Swap DV01", "fixed_income/swap_dv01.md"),
        ("DV01", "fixed_income/dv01.md"),
        ("Repo and financing", "fixed_income/repo_and_financing.md"),
    ],
    "fixed_income/z_spread.md": [
        ("Curve construction", "fixed_income/curve_construction.md"),
        ("OAS", "fixed_income/oas.md"),
        ("Spread duration", "fixed_income/spread_duration.md"),
    ],
    "fx/cross_currency_basis.md": [
        ("FX spot and forward", "fx/spot_and_forward.md"),
        ("FX carry", "fx/fx_carry.md"),
        ("Swap spread (the fixed-income analogue)", "fixed_income/swap_spread.md"),
    ],
    "fx/fx_carry.md": [
        ("FX spot and forward", "fx/spot_and_forward.md"),
        ("Cross-currency basis", "fx/cross_currency_basis.md"),
    ],
    "fx/spot_and_forward.md": [
        ("Cross-currency basis", "fx/cross_currency_basis.md"),
        ("FX carry", "fx/fx_carry.md"),
        ("Forward rates (same no-arbitrage logic)", "fixed_income/forward_rates.md"),
    ],
    "alternatives/alternatives_overview.md": [
        ("ESG and sustainable investing", "alternatives/esg_and_sustainable_investing.md"),
        ("Leveraged loans", "fixed_income/leveraged_loans.md"),
        ("Liability-driven investing", "concepts/liability_driven_investing.md"),
        ("Strategic and tactical asset allocation", "concepts/strategic_and_tactical_asset_allocation.md"),
    ],
    "alternatives/esg_and_sustainable_investing.md": [
        ("Alternative investments overview", "alternatives/alternatives_overview.md"),
        ("Fundamental credit analysis", "fixed_income/fundamental_credit_analysis.md"),
        ("Liquidity", "concepts/liquidity.md"),
    ],
}


def relpath(src_key, target_key):
    src_dir = (REF_ROOT / src_key).parent
    target = REF_ROOT / target_key
    return os.path.relpath(target, src_dir)


def bullet_list(src_key, links):
    lines = []
    for text, target_key in links:
        lines.append(f"- [{text}]({relpath(src_key, target_key)})")
    return "\n".join(lines) + "\n"


def rewrite_related_section(src_key):
    path = REF_ROOT / src_key
    text = path.read_text()
    links = RELATED.get(src_key)
    if links is None:
        return False
    new_block = "## Related\n" + bullet_list(src_key, links)

    heading_re = re.compile(r"^## Related\s*\n", re.MULTILINE)
    m = heading_re.search(text)
    if m:
        rest = text[m.end():]
        next_heading = re.search(r"^## ", rest, re.MULTILINE)
        tail = rest[next_heading.start():] if next_heading else ""
        new_text = text[:m.start()] + new_block + ("\n" + tail if tail else "")
    else:
        new_text = text.rstrip("\n") + "\n\n" + new_block

    if new_text != text:
        path.write_text(new_text)
        return True
    return False


def rewrite_reference_index():
    path = ROOT / "reference" / "index.md"
    # Grouped by (section, subsection), preserving SECTIONS order, emitting
    # one H2 per new section and one H3 per subsection.
    glossary_callout = (
        "\nNew to this vocabulary? Start with the [Glossary](glossary.md) "
        "for a one-line-per-term cheat sheet before diving into a full page.\n"
    )
    out = ["# PM/FICC Reference Index\n", glossary_callout]
    seen_sections = set()
    for section, subsection, items in SECTIONS:
        if section not in seen_sections:
            out.append(f"\n## {section}\n")
            seen_sections.add(section)
        if subsection:
            out.append(f"\n### {subsection}\n")
        for target_key, title in items:
            out.append(f"- [{title}]({target_key})")
        if not subsection:
            out.append("")
    out.append(
        "\nMore pages should be added continuously using `templates/CONCEPT_TEMPLATE.md`.\n"
    )
    path.write_text("\n".join(out).replace("\n\n\n", "\n\n"))


def rewrite_curriculum_notebooks():
    path = ROOT / "curriculum" / "bootcamp_01_foundations" / "README.md"
    text = path.read_text()

    def replace_bullet(m):
        indent, nb_path = m.group(1), m.group(2)
        full = nb_path if nb_path.startswith("notebooks/") else f"notebooks/{nb_path}"
        # bootcamp README uses paths both with and without the leading
        # "notebooks/<track>/" prefix on later lines in the same block -
        # resolve against known notebooks by basename if a direct hit misses.
        title = NOTEBOOKS.get(full)
        if title is None:
            base = Path(nb_path).name
            for k, v in NOTEBOOKS.items():
                if k.endswith(base):
                    full, title = k, v
                    break
        if title is None:
            return m.group(0)
        rel = os.path.relpath(ROOT / full, path.parent)
        return f"{indent}[{title}]({rel})"

    new_text = re.sub(
        r"^(- )`(notebooks/[^`]+\.ipynb|[0-9]{2}_[^`]+\.ipynb)`",
        replace_bullet,
        text,
        flags=re.MULTILINE,
    )
    if new_text != text:
        path.write_text(new_text)


def rewrite_use_cases_index():
    path = ROOT / "use_cases" / "index.md"
    text = path.read_text()

    def replace_bullet(m):
        indent, uc_path = m.group(1), m.group(2)
        slug = uc_path.split("/")[0]
        title = dict(USE_CASES).get(slug)
        if title is None:
            return m.group(0)
        return f"{indent}[{title}]({uc_path})"

    # Bullets are written relative to use_cases/index.md itself, so paths
    # have no "use_cases/" prefix (e.g. "duration_hedging/README.md").
    new_text = re.sub(
        r"^(- )`([a-z_]+/README\.md)`",
        replace_bullet,
        text,
        flags=re.MULTILINE,
    )
    if new_text != text:
        path.write_text(new_text)


def main():
    updated = []
    for src_key in TITLES:
        if src_key not in RELATED:
            continue
        if rewrite_related_section(src_key):
            updated.append(src_key)

    missing = [k for k in TITLES if k not in RELATED and k != "concepts/agentic_pm_analytics.md"]
    if missing:
        print("WARNING - reference pages with no RELATED entry:", missing)

    rewrite_reference_index()
    rewrite_curriculum_notebooks()
    rewrite_use_cases_index()

    print(f"Linkified {len(updated)} reference pages, reference/index.md, "
          f"curriculum notebooks, and use_cases/index.md")


if __name__ == "__main__":
    main()
