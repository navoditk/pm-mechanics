import numpy as np
from scipy.optimize import brentq

from .bond import bond_cashflows
from .curve import interpolate_zero_rate


def spread_pnl(market_value, spread_duration, spread_change_bp):
    delta_spread = spread_change_bp / 10_000.0
    return -market_value * spread_duration * delta_spread


def z_spread(price, face, coupon_rate, years, frequency, curve_tenors, curve_rates):
    """Constant spread over the interpolated zero curve that reprices the
    bond to `price`. Solved by root-finding, not closed-form.
    """
    times, flows = bond_cashflows(face, coupon_rate, years, frequency)

    def _price_at_spread(spread):
        discounted = 0.0
        for t, cf in zip(times, flows):
            z = interpolate_zero_rate(t, curve_tenors, curve_rates)
            discounted += cf / (1 + (z + spread) / frequency) ** (t * frequency)
        return discounted - price

    return brentq(_price_at_spread, -0.05, 0.50)


def survival_probability(hazard_rate, t):
    """Probability of no default by time t, under a constant hazard rate."""
    return float(np.exp(-hazard_rate * t))


def expected_loss(notional, default_probability, recovery_rate):
    return notional * default_probability * (1 - recovery_rate)


def credit_spread_from_hazard(hazard_rate, recovery_rate):
    """Approximate par CDS/credit spread implied by a constant hazard rate
    and recovery assumption: spread ~= hazard_rate * (1 - recovery_rate).
    """
    return hazard_rate * (1 - recovery_rate)


def cds_bond_basis(cds_spread, bond_spread):
    return cds_spread - bond_spread


def index_intrinsic_spread(constituent_spreads, weights=None):
    """Intrinsic value of a CDS index: the weighted average of its
    constituent single-name CDS spreads. Real intrinsic-value
    calculations PV01-weight the constituents (each name's duration-like
    sensitivity); this repo's version uses simple weights (equal-weighted
    if none given) as a transparent approximation - see
    reference/fixed_income/credit_indices.md.
    """
    spreads = np.asarray(constituent_spreads, dtype=float)
    if weights is None:
        weights = np.ones_like(spreads) / len(spreads)
    else:
        weights = np.asarray(weights, dtype=float)
    return float(np.average(spreads, weights=weights))


def index_basis(index_spread, intrinsic_spread):
    """Index basis: the traded index spread minus its intrinsic value.
    A nonzero basis is the classic index-vs-constituents relative-value
    trade - whichever side offers more spread for the same underlying
    risk is the one to sell protection on, financed by buying protection
    on the other side. See reference/fixed_income/credit_indices.md for
    which side that actually is - the sign convention is easy to get
    backwards, so this function stays purely mechanical.
    """
    return index_spread - intrinsic_spread


def leverage_ratio(total_debt, ebitda):
    """Debt / EBITDA - the standard leverage measure in credit analysis
    and loan covenants. Higher = more leveraged = more credit risk.
    """
    return total_debt / ebitda


def interest_coverage_ratio(ebitda, interest_expense):
    """EBITDA / interest expense - how many times over a borrower could
    pay its interest bill from earnings. Higher = safer; a minimum
    threshold, not a maximum (opposite direction from leverage_ratio).
    """
    return ebitda / interest_expense


def fixed_charge_coverage_ratio(ebitda, interest_expense, mandatory_principal_payments):
    """EBITDA / (interest expense + mandatory principal payments) - a
    stricter coverage measure than interest_coverage_ratio, since
    scheduled debt amortization has to be paid in cash just like
    interest, not just refinanced indefinitely.
    """
    return ebitda / (interest_expense + mandatory_principal_payments)
