import numpy as np
import pytest

from pm.equity.capm import beta, capm_expected_return, equity_risk_premium, jensens_alpha
from pm.equity.factors import active_share, style_tilt
from pm.equity.income import (
    buyback_yield,
    dividend_yield,
    payout_ratio,
    shareholder_yield,
    total_shareholder_return,
)
from pm.equity.valuation import (
    gordon_growth_value,
    implied_growth_from_price,
    justified_pe,
    peg_ratio,
    two_stage_ddm_value,
)


def test_gordon_growth_hand_example():
    # D1=2, r=9%, g=4% -> V = 2 / 0.05 = 40
    assert np.isclose(gordon_growth_value(2.0, 0.09, 0.04), 40.0)


def test_gordon_growth_at_zero_growth_prices_a_preferred_stock():
    # growth_rate=0 collapses Gordon growth to a plain perpetuity,
    # D1 / r - the standard preferred-stock valuation formula. See
    # reference/fixed_income/preferred_securities.md.
    assert np.isclose(
        gordon_growth_value(dividend_next=2.0, required_return=0.08, growth_rate=0.0), 25.0
    )


def test_gordon_growth_rejects_growth_at_or_above_required_return():
    with pytest.raises(ValueError):
        gordon_growth_value(2.0, 0.05, 0.05)


def test_two_stage_ddm_collapses_to_gordon_growth_at_constant_growth():
    # if high_growth == terminal_growth, the two-stage split is just an
    # algebraic decomposition of a single constant-growth stream - it
    # must reproduce gordon_growth_value applied to the first dividend.
    d0, g, r = 1.0, 0.04, 0.09
    for years in (1, 3, 10):
        two_stage = two_stage_ddm_value(d0, g, years, g, r)
        single_stage = gordon_growth_value(d0 * (1 + g), r, g)
        assert np.isclose(two_stage, single_stage)


def test_two_stage_ddm_high_growth_exceeds_constant_growth_value():
    d0, r = 1.0, 0.09
    high = two_stage_ddm_value(d0, 0.15, 5, 0.04, r)
    flat = two_stage_ddm_value(d0, 0.04, 5, 0.04, r)
    assert high > flat


def test_implied_growth_round_trips_through_gordon_growth():
    price, d1, r = 40.0, 2.0, 0.09
    g = implied_growth_from_price(price, d1, r)
    assert np.isclose(gordon_growth_value(d1, r, g), price)


def test_justified_pe_hand_example():
    # payout=40%, r=9%, g=5% -> PE = 0.4 / 0.04 = 10
    assert np.isclose(justified_pe(0.40, 0.09, 0.05), 10.0)


def test_peg_ratio_hand_example():
    assert np.isclose(peg_ratio(15.0, 15.0), 1.0)


def test_beta_recovers_exact_linear_relationship():
    market = np.array([0.01, 0.02, -0.01, 0.03, 0.00])
    stock = 1.5 * market
    assert np.isclose(beta(stock, market), 1.5)


def test_capm_expected_return_hand_example():
    assert np.isclose(capm_expected_return(0.03, 1.2, 0.05), 0.09)


def test_equity_risk_premium_hand_example():
    assert np.isclose(equity_risk_premium(0.08, 0.03), 0.05)


def test_jensens_alpha_hand_example():
    # rf=3%, beta=1.2, market=8% -> expected = 3% + 1.2*5% = 9%
    # realized=12% -> alpha = 3%
    alpha = jensens_alpha(
        realized_return=0.12, risk_free_rate=0.03, beta_value=1.2, market_return=0.08
    )
    assert np.isclose(alpha, 0.03)


def test_jensens_alpha_zero_when_realized_matches_capm():
    alpha = jensens_alpha(
        realized_return=0.09, risk_free_rate=0.03, beta_value=1.2, market_return=0.08
    )
    assert np.isclose(alpha, 0.0)


def test_active_share_matches_benchmark_basics_example():
    # same 60/40 vs 50/50 example as reference/concepts/benchmark_basics.md
    assert np.isclose(active_share([0.6, 0.4], [0.5, 0.5]), 0.10)


def test_active_share_zero_for_matched_weights():
    assert np.isclose(active_share([0.3, 0.7], [0.3, 0.7]), 0.0)


def test_style_tilt_hand_example():
    assert np.isclose(style_tilt(0.8, 0.3), 0.5)


def test_dividend_yield_hand_example():
    assert np.isclose(dividend_yield(2.0, 50.0), 0.04)


def test_buyback_yield_hand_example():
    assert np.isclose(buyback_yield(500.0, 10_000.0), 0.05)


def test_shareholder_yield_sums_dividend_and_buyback():
    assert np.isclose(shareholder_yield(0.04, 0.05), 0.09)


def test_total_shareholder_return_hand_example():
    assert np.isclose(total_shareholder_return(100.0, 108.0, 2.0), 0.10)


def test_payout_ratio_hand_example():
    assert np.isclose(payout_ratio(2.0, 5.0), 0.40)
