import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm


def _d1_d2(spot, strike, rate, volatility, time_to_expiry, dividend_yield=0.0):
    d1 = (
        np.log(spot / strike) + (rate - dividend_yield + 0.5 * volatility**2) * time_to_expiry
    ) / (volatility * np.sqrt(time_to_expiry))
    d2 = d1 - volatility * np.sqrt(time_to_expiry)
    return d1, d2


def black_scholes_call_price(spot, strike, rate, volatility, time_to_expiry, dividend_yield=0.0):
    """European call under Black-Scholes-Merton, with a continuous
    dividend yield (0.0 for a non-dividend-paying stock; set to a foreign
    risk-free rate for a Garman-Kohlhagen FX option).
    """
    d1, d2 = _d1_d2(spot, strike, rate, volatility, time_to_expiry, dividend_yield)
    return spot * np.exp(-dividend_yield * time_to_expiry) * norm.cdf(d1) - strike * np.exp(
        -rate * time_to_expiry
    ) * norm.cdf(d2)


def black_scholes_put_price(spot, strike, rate, volatility, time_to_expiry, dividend_yield=0.0):
    """European put under Black-Scholes-Merton. See black_scholes_call_price."""
    d1, d2 = _d1_d2(spot, strike, rate, volatility, time_to_expiry, dividend_yield)
    return strike * np.exp(-rate * time_to_expiry) * norm.cdf(-d2) - spot * np.exp(
        -dividend_yield * time_to_expiry
    ) * norm.cdf(-d1)


def put_call_parity_residual(
    call_price, put_price, spot, strike, rate, time_to_expiry, dividend_yield=0.0
):
    """C - P should equal S*exp(-qT) - K*exp(-rT) for European options on
    the same underlying/strike/expiry - this residual is 0 when parity
    holds and nonzero when a quoted call/put pair is inconsistent
    (an arbitrage, absent transaction costs).
    """
    return (call_price - put_price) - (
        spot * np.exp(-dividend_yield * time_to_expiry) - strike * np.exp(-rate * time_to_expiry)
    )


def delta_call(spot, strike, rate, volatility, time_to_expiry, dividend_yield=0.0):
    """Price sensitivity to a $1 move in the underlying: dC/dS. In [0, 1]."""
    d1, _ = _d1_d2(spot, strike, rate, volatility, time_to_expiry, dividend_yield)
    return float(np.exp(-dividend_yield * time_to_expiry) * norm.cdf(d1))


def delta_put(spot, strike, rate, volatility, time_to_expiry, dividend_yield=0.0):
    """dP/dS. In [-1, 0] - equals delta_call - exp(-qT) by put-call parity."""
    d1, _ = _d1_d2(spot, strike, rate, volatility, time_to_expiry, dividend_yield)
    return float(-np.exp(-dividend_yield * time_to_expiry) * norm.cdf(-d1))


def gamma(spot, strike, rate, volatility, time_to_expiry, dividend_yield=0.0):
    """d(delta)/dS - identical for a call and a put at the same strike/expiry."""
    d1, _ = _d1_d2(spot, strike, rate, volatility, time_to_expiry, dividend_yield)
    return float(
        np.exp(-dividend_yield * time_to_expiry)
        * norm.pdf(d1)
        / (spot * volatility * np.sqrt(time_to_expiry))
    )


def vega(spot, strike, rate, volatility, time_to_expiry, dividend_yield=0.0):
    """dV/d(volatility), per 1.0 (100 vol points) of volatility - identical
    for a call and a put at the same strike/expiry.
    """
    d1, _ = _d1_d2(spot, strike, rate, volatility, time_to_expiry, dividend_yield)
    return float(
        spot * np.exp(-dividend_yield * time_to_expiry) * norm.pdf(d1) * np.sqrt(time_to_expiry)
    )


def theta_call(spot, strike, rate, volatility, time_to_expiry, dividend_yield=0.0):
    """-dC/d(time_to_expiry), i.e. value lost per year as expiry
    approaches with everything else held fixed ("time decay").
    """
    d1, d2 = _d1_d2(spot, strike, rate, volatility, time_to_expiry, dividend_yield)
    term1 = (
        -spot
        * np.exp(-dividend_yield * time_to_expiry)
        * norm.pdf(d1)
        * volatility
        / (2 * np.sqrt(time_to_expiry))
    )
    term2 = dividend_yield * spot * np.exp(-dividend_yield * time_to_expiry) * norm.cdf(d1)
    term3 = -rate * strike * np.exp(-rate * time_to_expiry) * norm.cdf(d2)
    return float(term1 + term2 + term3)


def theta_put(spot, strike, rate, volatility, time_to_expiry, dividend_yield=0.0):
    """-dP/d(time_to_expiry). See theta_call."""
    d1, d2 = _d1_d2(spot, strike, rate, volatility, time_to_expiry, dividend_yield)
    term1 = (
        -spot
        * np.exp(-dividend_yield * time_to_expiry)
        * norm.pdf(d1)
        * volatility
        / (2 * np.sqrt(time_to_expiry))
    )
    term2 = -dividend_yield * spot * np.exp(-dividend_yield * time_to_expiry) * norm.cdf(-d1)
    term3 = rate * strike * np.exp(-rate * time_to_expiry) * norm.cdf(-d2)
    return float(term1 + term2 + term3)


def rho_call(spot, strike, rate, volatility, time_to_expiry, dividend_yield=0.0):
    """dC/dr, per 1.0 (100%) of rate."""
    _, d2 = _d1_d2(spot, strike, rate, volatility, time_to_expiry, dividend_yield)
    return float(strike * time_to_expiry * np.exp(-rate * time_to_expiry) * norm.cdf(d2))


def rho_put(spot, strike, rate, volatility, time_to_expiry, dividend_yield=0.0):
    """dP/dr, per 1.0 (100%) of rate."""
    _, d2 = _d1_d2(spot, strike, rate, volatility, time_to_expiry, dividend_yield)
    return float(-strike * time_to_expiry * np.exp(-rate * time_to_expiry) * norm.cdf(-d2))


def implied_volatility_call(market_price, spot, strike, rate, time_to_expiry, dividend_yield=0.0):
    """Volatility that reprices black_scholes_call_price to market_price,
    solved by bisection (brentq) over a wide, safely bracketing vol range.
    """

    def objective(vol):
        return (
            black_scholes_call_price(spot, strike, rate, vol, time_to_expiry, dividend_yield)
            - market_price
        )

    return float(brentq(objective, 1e-6, 5.0))


def implied_volatility_put(market_price, spot, strike, rate, time_to_expiry, dividend_yield=0.0):
    """Volatility that reprices black_scholes_put_price to market_price. See implied_volatility_call."""

    def objective(vol):
        return (
            black_scholes_put_price(spot, strike, rate, vol, time_to_expiry, dividend_yield)
            - market_price
        )

    return float(brentq(objective, 1e-6, 5.0))


def black76_call_price(forward, strike, rate, volatility, time_to_expiry):
    """European call on a forward/futures price (Black-76) - the model
    underlying options quoted on a forward rather than a spot price:
    commodity futures options directly, and (with an annuity/discount-
    factor layer this repo doesn't build) the base math behind swaptions
    and caps/floors too - see
    reference/derivatives/options_on_forwards_and_rates_options.md.
    Identical to black_scholes_call_price with dividend_yield=rate and
    spot replaced by forward (that substitution makes the S*exp((r-q)T)
    forward-value term equal the forward price directly).
    """
    d1 = (np.log(forward / strike) + 0.5 * volatility**2 * time_to_expiry) / (
        volatility * np.sqrt(time_to_expiry)
    )
    d2 = d1 - volatility * np.sqrt(time_to_expiry)
    return float(np.exp(-rate * time_to_expiry) * (forward * norm.cdf(d1) - strike * norm.cdf(d2)))


def black76_put_price(forward, strike, rate, volatility, time_to_expiry):
    """European put on a forward/futures price (Black-76). See black76_call_price."""
    d1 = (np.log(forward / strike) + 0.5 * volatility**2 * time_to_expiry) / (
        volatility * np.sqrt(time_to_expiry)
    )
    d2 = d1 - volatility * np.sqrt(time_to_expiry)
    return float(
        np.exp(-rate * time_to_expiry) * (strike * norm.cdf(-d2) - forward * norm.cdf(-d1))
    )
