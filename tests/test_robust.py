import numpy as np
import pytest

from pm.optimization import mean_variance, minimum_variance
from pm.risk import component_risk_contribution
from pm.robust import (
    black_litterman_posterior,
    market_implied_returns,
    risk_parity_weights,
    scenario_robust_weights,
    shrink_covariance,
)


def test_shrink_covariance_full_shrinkage_is_diagonal():
    cov = [[0.04, 0.01], [0.01, 0.09]]
    shrunk = shrink_covariance(cov, shrinkage=1.0)
    assert np.isclose(shrunk[0][1], 0.0)
    assert np.isclose(shrunk[0][0], 0.04)
    assert np.isclose(shrunk[1][1], 0.09)


def test_shrink_covariance_zero_shrinkage_unchanged():
    cov = np.array([[0.04, 0.01], [0.01, 0.09]])
    shrunk = shrink_covariance(cov, shrinkage=0.0)
    assert np.allclose(shrunk, cov)


def test_market_implied_returns_hand_example():
    sigma = np.array([[0.04, 0.01], [0.01, 0.09]])
    w_market = np.array([0.6, 0.4])
    pi = market_implied_returns(risk_aversion=3.0, covariance=sigma, market_weights=w_market)
    expected = 3.0 * (sigma @ w_market)
    assert np.allclose(pi, expected)


def test_black_litterman_no_confidence_view_leaves_prior_unchanged():
    prior = np.array([0.05, 0.07])
    sigma = np.array([[0.04, 0.01], [0.01, 0.09]])
    P = np.array([[1.0, 0.0]])
    Q = np.array([0.20])  # wildly different from prior
    omega_huge = np.array([[1e6]])
    posterior_mean, _ = black_litterman_posterior(prior, sigma, P, Q, omega_huge)
    assert np.allclose(posterior_mean, prior, atol=1e-4)


def test_black_litterman_confident_view_shifts_posterior_toward_it():
    prior = np.array([0.05, 0.07])
    sigma = np.array([[0.04, 0.01], [0.01, 0.09]])
    P = np.array([[1.0, 0.0]])
    Q = np.array([0.10])
    omega_confident = np.array([[0.0001]])
    posterior_mean, _ = black_litterman_posterior(prior, sigma, P, Q, omega_confident)
    assert posterior_mean[0] > prior[0]
    assert abs(posterior_mean[0] - 0.10) < abs(prior[0] - 0.10)


def test_risk_parity_equal_vol_uncorrelated_gives_equal_weights():
    cov = [[0.04, 0.0], [0.0, 0.04]]
    w = risk_parity_weights(cov)
    assert np.allclose(w, [0.5, 0.5], atol=1e-3)


def test_risk_parity_equalizes_risk_contribution_not_weights():
    cov = np.array([[0.04, 0.0], [0.0, 0.16]])
    w = risk_parity_weights(cov)
    contributions = component_risk_contribution(w, cov)
    assert np.isclose(contributions[0], contributions[1], atol=1e-3)
    assert not np.isclose(w[0], w[1], atol=1e-2)


def test_scenario_robust_weights_symmetric_scenarios_give_equal_weights():
    scenario_returns = [
        [0.10, -0.05],
        [-0.05, 0.10],
    ]
    w = scenario_robust_weights(scenario_returns)
    assert np.allclose(w, [0.5, 0.5], atol=1e-3)


def test_market_implied_returns_round_trips_through_mean_variance():
    """market_implied_returns inverts mean_variance's first-order condition
    (mu = risk_aversion * Sigma * w) - this is the actual Black-Litterman
    workflow (reverse-optimize market weights into a prior, then
    re-optimize) and is the reason mean_variance carries a 1/2 on its risk
    term. Without that 1/2 this round trip closes at risk_aversion/2
    instead of risk_aversion, which no other test in this file catches
    since none of them call both functions together.
    """
    sigma = np.array([[0.04, 0.01], [0.01, 0.09]])
    w_market = np.array([0.6, 0.4])
    risk_aversion = 3.0
    pi = market_implied_returns(risk_aversion, sigma, w_market)
    w_recovered = mean_variance(pi, sigma, risk_aversion=risk_aversion, long_only=False)
    assert np.allclose(w_recovered, w_market, atol=1e-4)


def test_infeasible_minimum_variance_raises_instead_of_returning_none():
    # 5 long-only assets capped at 10% each can't sum to 1 - infeasible.
    cov = np.eye(5) * 0.04
    with pytest.raises(ValueError, match="did not reach an optimal solution"):
        minimum_variance(cov, long_only=True, max_weight=0.1)


def test_unbounded_mean_variance_raises_instead_of_returning_none():
    # long/short with no bound on w and positive expected returns on a
    # perfectly correlated pair is unbounded (scale up the winning leg
    # without limit) - the solver can't reach an optimal point.
    cov = [[0.04, 0.04], [0.04, 0.04]]
    with pytest.raises(ValueError, match="did not reach an optimal solution"):
        mean_variance([0.10, 0.02], cov, risk_aversion=1.0, long_only=False)
