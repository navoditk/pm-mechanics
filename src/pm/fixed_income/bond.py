import numpy as np


def bond_cashflows(face=100.0, coupon_rate=0.05, years=5.0, frequency=2):
    n = round(years * frequency)
    coupon = face * coupon_rate / frequency
    flows = np.full(n, coupon, dtype=float)
    flows[-1] += face
    periods = np.arange(1, n + 1)
    times = periods / frequency
    return times, flows


def bond_price(ytm, face=100.0, coupon_rate=0.05, years=5.0, frequency=2):
    _, flows = bond_cashflows(face, coupon_rate, years, frequency)
    periods = np.arange(1, len(flows) + 1)
    discount = (1 + ytm / frequency) ** periods
    return float(np.sum(flows / discount))
