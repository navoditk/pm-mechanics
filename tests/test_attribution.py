import numpy as np

from pm.attribution import (
    brinson_attribution,
    fixed_income_return_decomposition,
    rebalancing_trades,
    total_attribution,
    transaction_cost,
)


def test_total_attribution_hand_example():
    assert np.isclose(total_attribution({"a": 100.0, "b": -30.0}), 70.0)


def test_brinson_effects_sum_to_active_return():
    wp = np.array([0.6, 0.4])
    wb = np.array([0.5, 0.5])
    rp = np.array([0.10, 0.02])
    rb = np.array([0.08, 0.03])

    allocation, selection, interaction = brinson_attribution(wp, wb, rp, rb)
    active_return = wp @ rp - wb @ rb

    assert np.isclose(allocation.sum() + selection.sum() + interaction.sum(), active_return)


def test_fixed_income_return_decomposition_sums_to_total():
    result = fixed_income_return_decomposition(carry=0.02, curve_effect=-0.01, spread_effect=0.005)
    assert np.isclose(result["total"], 0.015)


def test_transaction_cost_hand_example():
    assert np.isclose(transaction_cost(1_000_000, 5), 500.0)


def test_rebalancing_trades_hand_example():
    trades = rebalancing_trades([0.6, 0.4], [0.5, 0.5], 1_000_000)
    assert np.allclose(trades, [-100_000, 100_000])
