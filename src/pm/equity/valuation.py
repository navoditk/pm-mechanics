def gordon_growth_value(dividend_next, required_return, growth_rate):
    """Gordon growth (constant-growth) DDM: V = D1 / (r - g)."""
    if required_return <= growth_rate:
        raise ValueError("required_return must exceed growth_rate for the model to converge.")
    return dividend_next / (required_return - growth_rate)


def two_stage_ddm_value(
    dividend_now, high_growth, high_growth_years, terminal_growth, required_return
):
    """Two-stage DDM: dividends grow at high_growth for high_growth_years,
    then at terminal_growth forever. Sums the discounted high-growth
    dividends plus the discounted Gordon-growth terminal value.
    """
    if required_return <= terminal_growth:
        raise ValueError(
            "required_return must exceed terminal_growth for the terminal value to converge."
        )
    pv = 0.0
    dividend = dividend_now
    for year in range(1, high_growth_years + 1):
        dividend *= 1 + high_growth
        pv += dividend / (1 + required_return) ** year
    terminal_dividend = dividend * (1 + terminal_growth)
    terminal_value = terminal_dividend / (required_return - terminal_growth)
    pv += terminal_value / (1 + required_return) ** high_growth_years
    return pv


def implied_growth_from_price(price, dividend_next, required_return):
    """Invert the Gordon growth model to solve for the growth rate the
    market is pricing in, given price and required return instead of growth.
    """
    return required_return - dividend_next / price


def justified_pe(payout_ratio, required_return, growth_rate):
    """Fundamental P/E implied by the Gordon growth model:
    P/E = payout_ratio / (required_return - growth_rate).
    """
    if required_return <= growth_rate:
        raise ValueError("required_return must exceed growth_rate for the model to converge.")
    return payout_ratio / (required_return - growth_rate)


def peg_ratio(pe_ratio, growth_rate_pct):
    """P/E divided by expected growth expressed in percentage points
    (e.g. 15% growth -> pass 15, not 0.15) - the market convention.
    """
    return pe_ratio / growth_rate_pct
