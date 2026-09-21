import numpy as np

from pm.risk import expected_shortfall, parametric_var


def test_parametric_var_95_hand_example():
    z_95 = 1.6448536269514722  # standard normal 95th percentile
    assert np.isclose(parametric_var(1_000_000, 0.02, confidence=0.95), 1_000_000 * 0.02 * z_95)


def test_var_scales_linearly_with_portfolio_value():
    small = parametric_var(1_000_000, 0.02, confidence=0.95)
    large = parametric_var(2_000_000, 0.02, confidence=0.95)
    assert np.isclose(large, 2 * small)


def test_expected_shortfall_exceeds_var_at_same_confidence():
    var = parametric_var(1_000_000, 0.02, confidence=0.95)
    es = expected_shortfall(1_000_000, 0.02, confidence=0.95)
    assert es > var
