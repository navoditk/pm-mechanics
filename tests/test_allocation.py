import numpy as np

from pm.allocation import funded_ratio, surplus


def test_funded_ratio_hand_example():
    assert np.isclose(funded_ratio(assets=90.0, liabilities=100.0), 0.90)


def test_funded_ratio_fully_funded_equals_one():
    assert np.isclose(funded_ratio(assets=100.0, liabilities=100.0), 1.0)


def test_surplus_hand_example():
    assert np.isclose(surplus(assets=90.0, liabilities=100.0), -10.0)


def test_surplus_positive_when_overfunded():
    assert surplus(assets=110.0, liabilities=100.0) > 0


def test_surplus_and_funded_ratio_agree_on_direction():
    # A plan that's underfunded (funded_ratio < 1) must have negative
    # surplus, and vice versa - these two metrics can't disagree.
    assets, liabilities = 85.0, 100.0
    assert (funded_ratio(assets, liabilities) < 1.0) == (surplus(assets, liabilities) < 0.0)
