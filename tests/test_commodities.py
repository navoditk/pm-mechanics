import numpy as np

from pm.commodities import commodity_curve_state, roll_yield


def test_roll_yield_positive_in_backwardation():
    assert np.isclose(roll_yield(near_price=80, far_price=78), (80 - 78) / 78)
    assert roll_yield(near_price=80, far_price=78) > 0


def test_roll_yield_negative_in_contango():
    assert roll_yield(near_price=78, far_price=80) < 0


def test_commodity_curve_state():
    assert commodity_curve_state(80, 78) == "backwardation"
    assert commodity_curve_state(78, 80) == "contango"
    assert commodity_curve_state(80, 80) == "flat"
