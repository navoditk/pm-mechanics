import numpy as np

from .bond import bond_cashflows, bond_price


def macaulay_duration(ytm, face=100.0, coupon_rate=0.05, years=5.0, frequency=2):
    times, flows = bond_cashflows(face, coupon_rate, years, frequency)
    periods = np.arange(1, len(flows) + 1)
    pv = flows / (1 + ytm / frequency) ** periods
    price = pv.sum()
    return float(np.sum(times * pv) / price)


def modified_duration(ytm, face=100.0, coupon_rate=0.05, years=5.0, frequency=2):
    mac = macaulay_duration(ytm, face, coupon_rate, years, frequency)
    return mac / (1 + ytm / frequency)


def dv01(ytm, face=100.0, coupon_rate=0.05, years=5.0, frequency=2):
    p = bond_price(ytm, face, coupon_rate, years, frequency)
    d = modified_duration(ytm, face, coupon_rate, years, frequency)
    return d * p * 1e-4


def convexity(ytm, face=100.0, coupon_rate=0.05, years=5.0, frequency=2):
    """Second-order price sensitivity, for use in
    dP/P ~= -modified_duration*dy + 0.5*convexity*dy**2.
    """
    _, flows = bond_cashflows(face, coupon_rate, years, frequency)
    periods = np.arange(1, len(flows) + 1)
    pv = flows / (1 + ytm / frequency) ** periods
    price = pv.sum()
    second_derivative = np.sum(pv * periods * (periods + 1)) / (
        frequency**2 * (1 + ytm / frequency) ** 2
    )
    return float(second_derivative / price)


def hedge_ratio(target_dv01, hedge_instrument_dv01):
    """Units of the hedge instrument needed to offset target_dv01.

    Negative = short the hedge instrument, positive = long it.
    """
    return -target_dv01 / hedge_instrument_dv01
