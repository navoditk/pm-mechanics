def fx_forward_rate(spot, domestic_rate, foreign_rate, years):
    """Covered interest parity (CIP) forward rate, simple interest.

    spot is quoted as domestic per foreign unit (e.g. USD per EUR).
    """
    return spot * (1 + domestic_rate * years) / (1 + foreign_rate * years)


def cross_currency_basis(market_forward, spot, domestic_rate, foreign_rate, years):
    """Deviation from CIP: the spread that, added to foreign_rate, would
    make fx_forward_rate match the observed market_forward.
    """
    implied_foreign_rate = ((1 + domestic_rate * years) * spot / market_forward - 1) / years
    return implied_foreign_rate - foreign_rate


def fx_carry(domestic_rate, foreign_rate):
    """Uncovered interest rate differential: the P&L from holding the
    foreign currency unhedged if spot doesn't move. Uncovered interest
    rate parity says spot should move to offset this - a carry trade bets
    that it won't, on average.
    """
    return foreign_rate - domestic_rate
