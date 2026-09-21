def breakeven_inflation(nominal_yield, real_yield):
    """Breakeven inflation rate: the market-implied average inflation rate
    over which a nominal Treasury and a same-maturity TIPS give the same
    return. breakeven = nominal_yield - real_yield.
    """
    return nominal_yield - real_yield


def tips_index_ratio(cpi_reference_current, cpi_reference_base):
    """TIPS index ratio: how much a TIPS's principal has grown from
    inflation since issuance. index_ratio = CPI_now / CPI_at_issuance.
    """
    return cpi_reference_current / cpi_reference_base


def tips_inflation_adjusted_principal(original_principal, index_ratio):
    """A TIPS's current (inflation-adjusted) principal - what its real
    coupon rate and final redemption are actually paid on, not the
    original face value.
    """
    return original_principal * index_ratio


def tips_coupon_payment(real_coupon_rate, inflation_adjusted_principal, frequency=2):
    """A TIPS coupon payment: the fixed real coupon rate applied to the
    *inflation-adjusted* principal, not the original face value - this is
    how a TIPS passes realized inflation through to the investor every
    period, not just at maturity.
    """
    return real_coupon_rate * inflation_adjusted_principal / frequency
