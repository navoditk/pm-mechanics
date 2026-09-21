import numpy as np
import pandas as pd
import pytest

from pm.returns import (
    cumulative_return,
    downside_deviation,
    log_returns,
    max_drawdown,
    money_weighted_return,
    portfolio_return,
    realized_volatility,
    sharpe_ratio,
    simple_returns,
)


def test_portfolio_return_hand_example():
    assert np.isclose(portfolio_return([0.10, -0.05], [0.60, 0.40]), 0.04)


def test_simple_returns_hand_example():
    prices = pd.Series([100.0, 110.0, 121.0])
    result = simple_returns(prices)
    assert np.isnan(result.iloc[0])
    assert np.allclose(result.iloc[1:], [0.10, 0.10])


def test_log_returns_hand_example():
    prices = pd.Series([100.0, 110.0])
    result = log_returns(prices)
    assert np.isnan(result.iloc[0])
    assert np.isclose(result.iloc[1], np.log(1.10))


def test_plus_50_minus_50_is_minus_25():
    assert np.isclose(cumulative_return([0.50, -0.50]), -0.25)


def test_sharpe_ratio_hand_example():
    returns = [0.02, 0.04, 0.03]
    assert np.isclose(sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=1), 3.0)


def test_zero_excess_return_gives_zero_sharpe():
    assert np.isclose(sharpe_ratio([0.01, -0.01], periods_per_year=1), 0.0)


def test_max_drawdown_hand_example():
    assert np.isclose(max_drawdown([0.10, -0.20, 0.05]), -0.20)


def test_metrics_compose_with_simple_returns_leading_nan():
    """simple_returns's leading NaN (asserted above) must not silently
    poison every downstream metric - it should be dropped, not propagated.
    Same 3 real observations as test_sharpe_ratio_hand_example /
    test_max_drawdown_hand_example, prefixed with the NaN
    prices->simple_returns actually produces.
    """
    prices = pd.Series([100.0, 102.0, 106.08, 109.2624])  # -> nan, 2%, 4%, 3%
    r = simple_returns(prices)
    assert np.isclose(sharpe_ratio(r, risk_free_rate=0.0, periods_per_year=1), 3.0)
    assert np.isclose(cumulative_return(r), 1.02 * 1.04 * 1.03 - 1)


def test_sharpe_ratio_rejects_an_all_nan_series():
    with pytest.raises(ValueError, match="finite observation"):
        sharpe_ratio([float("nan"), float("nan")])


def test_realized_volatility_matches_manual_std():
    returns = [0.02, -0.01, 0.03, 0.00, -0.02]
    expected = np.std(returns, ddof=1) * np.sqrt(12)
    assert np.isclose(realized_volatility(returns, periods_per_year=12), expected)


def test_realized_volatility_drops_leading_nan_from_simple_returns():
    prices = pd.Series([100.0, 102.0, 99.0, 103.0])
    r = simple_returns(prices)
    finite = r.dropna().to_numpy()
    expected = np.std(finite, ddof=1) * np.sqrt(12)
    assert np.isclose(realized_volatility(r, periods_per_year=12), expected)


def test_downside_deviation_hand_example():
    # shortfalls vs target=0: [0, -0.03, 0, -0.01]; mean(sq)=0.00025
    returns = [0.02, -0.03, 0.01, -0.01]
    expected = np.sqrt(0.00025) * np.sqrt(12)
    assert np.isclose(downside_deviation(returns, target=0.0, periods_per_year=12), expected)


def test_downside_deviation_zero_when_returns_never_fall_below_target():
    assert np.isclose(downside_deviation([0.01, 0.02, 0.03], target=0.0), 0.0)


def test_downside_deviation_less_than_or_equal_to_total_volatility():
    # downside deviation only counts shortfalls, so it can never exceed
    # the symmetric (upside+downside) volatility of the same series.
    returns = [0.05, -0.03, 0.02, -0.04, 0.01, -0.01]
    assert downside_deviation(returns, target=0.0) <= realized_volatility(returns)


def test_money_weighted_return_matches_simple_compounding_with_no_interim_flows():
    # -100 at t=0, +121 at t=2, no interim cash flows: should reduce to a
    # plain compound annual rate, (121/100)^(1/2) - 1 = 10%.
    mwr = money_weighted_return([-100.0, 121.0], [0.0, 2.0])
    assert np.isclose(mwr, 0.10, atol=1e-8)


def test_money_weighted_return_classic_twr_divergence_example():
    # The canonical TWR-vs-MWR textbook case: invest 100 at t=0; the
    # portfolio doubles to 200 by t=1 (period-1 return +100%), the
    # investor then contributes another 200 (now invested: 400); the
    # portfolio ends at 200 by t=2 (period-2 return -50%).
    # TWR = (1+1.00)*(1-0.50) - 1 = 0% - a wash.
    twr = cumulative_return([1.00, -0.50])
    assert np.isclose(twr, 0.0, atol=1e-8)
    # MWR weights the -50% period (where 400 was at risk) far more
    # heavily than the +100% period (where only 100 was at risk), so it
    # comes out sharply negative even though TWR is flat.
    mwr = money_weighted_return([-100.0, -200.0, 200.0], [0.0, 1.0, 2.0])
    assert np.isclose(mwr, -0.26794919, atol=1e-6)
    assert mwr < twr
