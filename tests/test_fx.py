import numpy as np

from pm.fx import cross_currency_basis, fx_carry, fx_forward_rate


def test_fx_forward_rate_hand_example():
    expected = 1.10 * 1.05 / 1.03
    assert np.isclose(fx_forward_rate(1.10, 0.05, 0.03, 1), expected)


def test_cross_currency_basis_zero_when_forward_matches_cip():
    forward = fx_forward_rate(1.10, 0.05, 0.03, 1)
    assert np.isclose(cross_currency_basis(forward, 1.10, 0.05, 0.03, 1), 0.0)


def test_fx_carry_hand_example():
    assert np.isclose(fx_carry(domestic_rate=0.02, foreign_rate=0.07), 0.05)
