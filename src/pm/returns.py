import numpy as np
import pandas as pd
from scipy.optimize import brentq

from ._utils import finite_array


def simple_returns(prices: pd.Series | pd.DataFrame):
    """Arithmetic period returns. The first element is NaN by construction
    (there is no prior price to compare against) - the metrics below drop
    it, so `prices -> simple_returns -> metric` composes directly.
    """
    return prices / prices.shift(1) - 1


def log_returns(prices: pd.Series | pd.DataFrame):
    """Log returns. First element is NaN by construction, as above."""
    return np.log(prices / prices.shift(1))


def portfolio_return(asset_returns, weights):
    r = np.asarray(asset_returns, dtype=float)
    w = np.asarray(weights, dtype=float)
    return float(w @ r)


def cumulative_return(returns):
    return float(np.prod(1 + finite_array(returns)) - 1)


def money_weighted_return(cash_flows, times):
    """Money-weighted return (dollar-weighted return / IRR): the constant
    periodic rate r that sets the NPV of all cash flows to zero,
    sum(cf_i / (1+r)^t_i) = 0.

    cash_flows are signed (negative = contribution/investment, positive =
    withdrawal/ending value); times are in years from the start of the
    measurement period. Unlike cumulative_return (the time-weighted
    return, which geometrically links sub-period returns and so is
    unaffected by cash-flow timing/size - see
    reference/concepts/performance_measurement.md), money-weighted return
    is exactly as sensitive to when and how much capital was invested as
    an investor's own realized dollar return actually is.

    Solved via bisection (brentq) over a wide (-0.99, 5.0) bracket. This
    assumes a single real root in that range, which holds for a typical
    contribution/withdrawal cash-flow pattern (one sign change, by
    Descartes' rule of signs) but is not guaranteed for cash flows that
    change sign more than once.
    """

    def npv(rate):
        return sum(cf / (1 + rate) ** t for cf, t in zip(cash_flows, times))

    return float(brentq(npv, -0.99, 5.0))


def sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=12):
    excess = finite_array(returns, min_size=2) - risk_free_rate / periods_per_year
    std = excess.std(ddof=1)
    if not np.isfinite(std) or std <= 0:
        raise ValueError("Excess return volatility must be positive and finite.")
    return float(excess.mean() / std * np.sqrt(periods_per_year))


def max_drawdown(returns):
    wealth = np.cumprod(1 + finite_array(returns))
    running_max = np.maximum.accumulate(wealth)
    drawdown = wealth / running_max - 1
    return float(drawdown.min())


def realized_volatility(returns, periods_per_year=12):
    """Ex-post portfolio volatility: annualized sample standard deviation
    of a realized return series - the natural counterpart to
    `pm.risk.portfolio_volatility`'s ex-ante (covariance-based) version.
    Comparing the two is how you check whether realized risk matched what
    a risk model predicted.
    """
    r = finite_array(returns, min_size=2)
    return float(r.std(ddof=1) * np.sqrt(periods_per_year))


def downside_deviation(returns, target=0.0, periods_per_year=12):
    """Semi-deviation below `target` (Sortino's risk measure): like
    volatility, but only shortfalls below the target count, not upside
    moves. Averaged over *all* periods, per Sortino's original
    definition - not just the shortfall periods - so a mostly-upside
    return series has a small downside deviation even if its total
    volatility (which treats upside and downside symmetrically) is large.
    """
    r = finite_array(returns, min_size=2)
    shortfall = np.minimum(r - target, 0.0)
    return float(np.sqrt(np.mean(shortfall**2)) * np.sqrt(periods_per_year))
