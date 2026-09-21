import numpy as np

from pm.factors import (
    factor_model_covariance,
    factor_variance_contribution,
    portfolio_factor_exposure,
    specific_variance_contribution,
)
from pm.risk import portfolio_variance


def test_factor_model_covariance_one_factor_hand_example():
    exposures = [[1.0], [0.5]]
    factor_covariance = [[0.04]]
    specific_variance = [0.01, 0.02]
    expected = [[0.05, 0.02], [0.02, 0.03]]
    result = factor_model_covariance(exposures, factor_covariance, specific_variance)
    assert np.allclose(result, expected)


def test_portfolio_factor_exposure_hand_example():
    weights = [0.5, 0.5]
    exposures = [[1.0, 0.0], [0.0, 1.0]]
    assert np.allclose(portfolio_factor_exposure(weights, exposures), [0.5, 0.5])


def test_factor_plus_specific_contribution_equals_total_variance():
    weights = [0.5, 0.5]
    exposures = [[1.0, 0.0], [0.0, 1.0]]
    factor_covariance = [[0.04, 0.0], [0.0, 0.09]]
    specific_variance = [0.01, 0.02]

    factor_var = factor_variance_contribution(weights, exposures, factor_covariance)
    specific_var = specific_variance_contribution(weights, specific_variance)

    total_cov = factor_model_covariance(exposures, factor_covariance, specific_variance)
    expected_total = portfolio_variance(weights, total_cov)

    assert np.isclose(factor_var + specific_var, expected_total)
