def carry_return(coupon_income, price, financing_rate, horizon_years=1.0):
    """Funding-adjusted carry: income earned from holding the bond, funded
    at financing_rate (e.g. repo), over horizon_years - the return earned
    purely from the passage of time if nothing else moves.

    carry = (running_yield - financing_rate) * horizon_years,
    running_yield = coupon_income / price.
    """
    running_yield = coupon_income / price
    return (running_yield - financing_rate) * horizon_years


def rolldown_return(modified_duration, current_yield, rolled_yield):
    """Price return from a bond 'sliding down' an unchanged yield curve as
    time passes: after horizon_years its remaining maturity is shorter, so
    (assuming the curve doesn't move) it now sits at rolled_yield instead
    of current_yield. On a normal upward-sloping curve rolled_yield is
    lower, giving a price gain; on an inverted curve rolled_yield is
    higher, giving a price loss ("negative roll").

    rolldown = -modified_duration * (rolled_yield - current_yield)
    """
    return -modified_duration * (rolled_yield - current_yield)


def carry_and_rolldown(
    coupon_income,
    price,
    financing_rate,
    modified_duration,
    current_yield,
    rolled_yield,
    horizon_years=1.0,
):
    """Total expected return from carry and rolldown combined - the return
    a bond position earns purely from the passage of time, assuming the
    yield curve doesn't move at all. See
    reference/fixed_income/carry_and_rolldown.md.
    """
    carry = carry_return(coupon_income, price, financing_rate, horizon_years)
    rolldown = rolldown_return(modified_duration, current_yield, rolled_yield)
    return carry + rolldown
