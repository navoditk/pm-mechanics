import numpy as np
import pytest

from pm.risk import (
    component_risk_contribution,
    group_risk_contribution,
    marginal_risk_contribution,
    portfolio_variance,
    portfolio_volatility,
)


def test_two_asset_variance_matches_expansion():
    v1, v2, rho = 0.20, 0.10, 0.25
    w = np.array([0.5, 0.5])
    cov = np.array([[v1 * v1, rho * v1 * v2], [rho * v1 * v2, v2 * v2]])
    expected = w[0] ** 2 * v1**2 + w[1] ** 2 * v2**2 + 2 * w[0] * w[1] * rho * v1 * v2
    assert np.isclose(portfolio_variance(w, cov), expected)


def test_marginal_risk_contribution_hand_example():
    cov = np.array([[0.04, 0.0], [0.0, 0.01]])
    w = np.array([0.5, 0.5])
    sigma_p = (0.5**2 * 0.04 + 0.5**2 * 0.01) ** 0.5
    expected = np.array([0.5 * 0.04, 0.5 * 0.01]) / sigma_p
    assert np.allclose(marginal_risk_contribution(w, cov), expected)


def test_component_risk_sums_to_volatility():
    cov = np.array([[0.04, 0.005], [0.005, 0.01]])
    w = np.array([0.5, 0.5])
    cr = component_risk_contribution(w, cov)
    assert np.isclose(cr.sum(), portfolio_volatility(w, cov))


def test_group_risk_contribution_sums_to_total_volatility():
    cov = np.array(
        [
            [0.04, 0.01, 0.00, 0.00],
            [0.01, 0.03, 0.00, 0.00],
            [0.00, 0.00, 0.02, 0.005],
            [0.00, 0.00, 0.005, 0.01],
        ]
    )
    w = np.array([0.3, 0.2, 0.25, 0.25])
    groups = ["Tech", "Tech", "Energy", "Energy"]
    grouped = group_risk_contribution(w, cov, groups)
    assert set(grouped) == {"Tech", "Energy"}
    assert np.isclose(sum(grouped.values()), portfolio_volatility(w, cov))


def test_group_risk_contribution_matches_component_when_groups_are_unique():
    cov = np.array([[0.04, 0.005], [0.005, 0.01]])
    w = np.array([0.5, 0.5])
    grouped = group_risk_contribution(w, cov, groups=["A", "B"])
    component = component_risk_contribution(w, cov)
    assert np.isclose(grouped["A"], component[0])
    assert np.isclose(grouped["B"], component[1])


def test_group_risk_contribution_rejects_mismatched_length():
    cov = np.array([[0.04, 0.0], [0.0, 0.01]])
    w = np.array([0.5, 0.5])
    with pytest.raises(ValueError, match="one label per asset"):
        group_risk_contribution(w, cov, groups=["A", "B", "C"])
