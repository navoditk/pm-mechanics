def dividend_yield(dividend_per_share, price):
    return dividend_per_share / price


def buyback_yield(buyback_value, market_cap):
    return buyback_value / market_cap


def shareholder_yield(dividend_yield_value, buyback_yield_value):
    return dividend_yield_value + buyback_yield_value


def total_shareholder_return(price_start, price_end, dividends_paid):
    """Price return plus dividends received, as a fraction of starting price."""
    return (price_end - price_start + dividends_paid) / price_start


def payout_ratio(dividend_per_share, earnings_per_share):
    return dividend_per_share / earnings_per_share
