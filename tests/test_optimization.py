import numpy as np
import pytest

from pm.active import tracking_error
from pm.optimization import (
    efficient_frontier,
    max_sharpe,
    mean_variance,
    min_tracking_error,
    minimum_variance,
)


def test_minimum_variance_two_asset_closed_form():
    cov = [[0.04, 0.0], [0.0, 0.01]]
    w = minimum_variance(cov)
    assert np.isclose(w[0], 0.2, atol=1e-3)
    assert np.isclose(w[1], 0.8, atol=1e-3)


def test_minimum_variance_weights_sum_to_one_and_long_only():
    cov = [[0.04, 0.01, 0.0], [0.01, 0.09, 0.02], [0.0, 0.02, 0.02]]
    w = minimum_variance(cov)
    assert np.isclose(w.sum(), 1.0, atol=1e-3)
    assert (w >= -1e-6).all()


def test_mean_variance_prefers_higher_return_asset():
    cov = [[0.04, 0.0], [0.0, 0.04]]
    w = mean_variance([0.10, 0.05], cov, risk_aversion=5.0)
    assert w[0] > w[1]


def test_efficient_frontier_endpoints_match_single_asset_weights():
    mu = [0.04, 0.08, 0.12]
    cov = [[0.02, 0.00, 0.00], [0.00, 0.03, 0.00], [0.00, 0.00, 0.05]]
    targets, _vols, weights = efficient_frontier(mu, cov, n_points=5)
    assert np.isclose(targets[0], 0.04) and np.isclose(targets[-1], 0.12)
    # lowest target is only achievable by holding 100% of the lowest-return asset
    assert np.allclose(weights[0], [1, 0, 0], atol=1e-3)
    assert np.allclose(weights[-1], [0, 0, 1], atol=1e-3)


def test_efficient_frontier_min_variance_point_has_lowest_volatility():
    mu = [0.04, 0.08, 0.12]
    cov = [[0.02, 0.005, 0.00], [0.005, 0.03, 0.01], [0.00, 0.01, 0.05]]
    _targets, vols, _weights = efficient_frontier(mu, cov, n_points=30)
    gmv_vol = np.sqrt(minimum_variance(cov) @ np.asarray(cov) @ minimum_variance(cov))
    # every frontier point (constrained to a specific target return) must
    # have volatility >= the unconstrained global-minimum-variance point
    assert vols.min() >= gmv_vol - 1e-6


def test_efficient_frontier_weights_sum_to_one_and_reprice_correctly():
    mu = [0.05, 0.09]
    cov = [[0.03, 0.01], [0.01, 0.04]]
    targets, _vols, weights = efficient_frontier(mu, cov, n_points=6)
    assert np.allclose(weights.sum(axis=1), 1.0, atol=1e-3)
    assert np.allclose(weights @ np.asarray(mu), targets, atol=1e-3)


def test_max_sharpe_unconstrained_closed_form_hand_example():
    # mu=[0.08,0.05], rf=0.02, cov=diag([0.04,0.01]) -> excess=[0.06,0.03]
    # Sigma^-1 @ excess = [0.06/0.04, 0.03/0.01] = [1.5, 3.0], sum=4.5
    # normalized -> [1/3, 2/3]
    w = max_sharpe([0.08, 0.05], [[0.04, 0.0], [0.0, 0.01]], risk_free_rate=0.02, long_only=False)
    assert np.allclose(w, [1 / 3, 2 / 3], atol=1e-3)


def test_max_sharpe_long_only_matches_unconstrained_when_already_long_only():
    # same inputs as above: the unconstrained tangency [1/3, 2/3] is
    # already long-only, so the constrained QP reformulation should
    # recover exactly the same answer as the closed form.
    cov = [[0.04, 0.0], [0.0, 0.01]]
    w = max_sharpe([0.08, 0.05], cov, risk_free_rate=0.02, long_only=True)
    assert np.allclose(w, [1 / 3, 2 / 3], atol=1e-3)


def test_max_sharpe_has_the_highest_sharpe_ratio_on_the_frontier():
    mu = [0.04, 0.08, 0.12]
    cov = [[0.02, 0.005, 0.00], [0.005, 0.03, 0.01], [0.00, 0.01, 0.05]]
    rf = 0.01
    w_tangency = max_sharpe(mu, cov, risk_free_rate=rf, long_only=True)
    tangency_sharpe = (np.asarray(mu) @ w_tangency - rf) / np.sqrt(
        w_tangency @ np.asarray(cov) @ w_tangency
    )

    _, vols, weights = efficient_frontier(mu, cov, n_points=25)
    frontier_sharpes = (weights @ np.asarray(mu) - rf) / vols
    assert tangency_sharpe >= frontier_sharpes.max() - 1e-6


def test_max_sharpe_rejects_no_excess_return_assets():
    with pytest.raises(ValueError, match="expected return above risk_free_rate"):
        max_sharpe([0.01, 0.02], [[0.04, 0.0], [0.0, 0.01]], risk_free_rate=0.05)


def test_min_tracking_error_with_no_extra_constraints_replicates_benchmark():
    wb = [0.4, 0.6]
    cov = [[0.04, 0.01], [0.01, 0.09]]
    w = min_tracking_error(wb, cov)
    assert np.allclose(w, wb, atol=1e-4)
    assert np.isclose(tracking_error(w, wb, cov), 0.0, atol=1e-4)


def test_min_tracking_error_with_max_weight_stays_close_to_benchmark():
    wb = [0.7, 0.3]
    cov = [[0.04, 0.01], [0.01, 0.09]]
    # benchmark itself violates max_weight=0.5, so TE cannot be exactly zero
    w = min_tracking_error(wb, cov, max_weight=0.5)
    assert np.isclose(w.sum(), 1.0, atol=1e-3)
    assert (w <= 0.5 + 1e-6).all()
    assert tracking_error(w, wb, cov) > 0
