import numpy as np

from ._utils import finite_array


def active_weights(portfolio_weights, benchmark_weights):
    return np.asarray(portfolio_weights, float) - np.asarray(benchmark_weights, float)


def tracking_error(portfolio_weights, benchmark_weights, covariance):
    a = active_weights(portfolio_weights, benchmark_weights)
    cov = np.asarray(covariance, float)
    return float(np.sqrt(a @ cov @ a))


def active_return(portfolio_return, benchmark_return):
    return float(portfolio_return - benchmark_return)


def realized_tracking_error(portfolio_returns, benchmark_returns, periods_per_year=12):
    """Ex-post (realized) tracking error: annualized volatility of the
    active-return series - the same active risk `tracking_error` computes
    ex-ante from a covariance matrix and active weights, but measured
    after the fact from an actual return history. See
    `information_ratio`, which uses this as its denominator.
    """
    p = np.asarray(portfolio_returns, dtype=float)
    b = np.asarray(benchmark_returns, dtype=float)
    if p.shape != b.shape:
        raise ValueError("portfolio_returns and benchmark_returns must be the same shape.")
    active = finite_array(p - b, min_size=2)
    std = active.std(ddof=1)
    if not np.isfinite(std) or std <= 0:
        raise ValueError("Active return volatility must be positive and finite.")
    return float(std * np.sqrt(periods_per_year))


def marginal_contribution_to_tracking_error(portfolio_weights, benchmark_weights, covariance):
    """How much tracking error changes per unit change in each asset's
    active weight, holding the others fixed - the number a benchmark-
    relative PM uses to decide which position to trim first to cut TE
    fastest. Mathematically `pm.risk.marginal_risk_contribution` applied
    at the active weights `a = w_p - w_b` instead of raw portfolio
    weights, against tracking error instead of total volatility.
    """
    a = active_weights(portfolio_weights, benchmark_weights)
    cov = np.asarray(covariance, dtype=float)
    te = tracking_error(portfolio_weights, benchmark_weights, cov)
    if te <= 0:
        raise ValueError("Tracking error must be positive.")
    return (cov @ a) / te


def component_contribution_to_tracking_error(portfolio_weights, benchmark_weights, covariance):
    """Each asset's marginal contribution to tracking error, scaled by its
    own active weight - sums exactly to total tracking error, so this is
    the per-position breakdown of "where is TE actually coming from."
    """
    a = active_weights(portfolio_weights, benchmark_weights)
    mcte = marginal_contribution_to_tracking_error(portfolio_weights, benchmark_weights, covariance)
    return a * mcte


def information_ratio(portfolio_returns, benchmark_returns, periods_per_year=12):
    """Realized information ratio: annualized mean active return per unit
    of active-return volatility, from matched portfolio/benchmark return
    series. This is the ex-post counterpart to `tracking_error` above,
    which is the ex-ante (covariance-based) version of the same active
    risk - see reference/concepts/information_ratio.md.
    """
    p = np.asarray(portfolio_returns, dtype=float)
    b = np.asarray(benchmark_returns, dtype=float)
    if p.shape != b.shape:
        raise ValueError("portfolio_returns and benchmark_returns must be the same shape.")
    active = finite_array(p - b, min_size=2)
    realized_te = active.std(ddof=1)
    if not np.isfinite(realized_te) or realized_te <= 0:
        raise ValueError(
            "Active return volatility (realized tracking error) must be positive and finite."
        )
    return float(active.mean() / realized_te * np.sqrt(periods_per_year))


def information_coefficient(forecasts, realized_returns):
    """Cross-sectional correlation between forecast scores (or ranks) and
    subsequently realized returns across a universe at one point in time -
    the standard measure of forecasting skill behind the Fundamental Law
    of Active Management. See reference/concepts/information_coefficient.md.
    """
    f = np.asarray(forecasts, dtype=float)
    r = np.asarray(realized_returns, dtype=float)
    if f.shape != r.shape:
        raise ValueError("forecasts and realized_returns must be the same shape.")
    if f.size < 2:
        raise ValueError("Need at least two observations to compute a correlation.")
    if np.std(f) == 0 or np.std(r) == 0:
        raise ValueError("forecasts and realized_returns must each have nonzero variance.")
    return float(np.corrcoef(f, r)[0, 1])


def effective_breadth(n_bets, average_correlation=0.0):
    """Number of independent bets (breadth), adjusted for correlation
    between them: `n_bets` truly independent forecasts are worth less the
    more they're correlated. At average_correlation=0, returns n_bets
    unchanged; at average_correlation=1 (every "bet" is really the same
    bet), returns 1 regardless of n_bets. See
    reference/concepts/fundamental_law.md.
    """
    n = float(n_bets)
    rho = float(average_correlation)
    return float(n / (1 + (n - 1) * rho))


def transfer_coefficient(actual_active_weights, unconstrained_active_weights):
    """How well real-world constraints let a portfolio implement its
    unconstrained-optimal active bets: the correlation between the active
    weights actually held and the active weights an unconstrained optimizer
    would have chosen from the same forecasts. TC=1 means constraints cost
    nothing; TC=0 means the held portfolio is unrelated to the ideal one.
    See reference/concepts/fundamental_law.md.
    """
    a = np.asarray(actual_active_weights, dtype=float)
    u = np.asarray(unconstrained_active_weights, dtype=float)
    if a.shape != u.shape:
        raise ValueError(
            "actual_active_weights and unconstrained_active_weights must be the same shape."
        )
    if np.std(a) == 0 or np.std(u) == 0:
        raise ValueError(
            "actual_active_weights and unconstrained_active_weights must each have nonzero variance."
        )
    return float(np.corrcoef(a, u)[0, 1])


def fundamental_law_ir(
    information_coefficient_value, breadth_value, transfer_coefficient_value=1.0
):
    """The Fundamental Law of Active Management (Grinold; extended by
    Clarke, de Silva & Thorley to include the transfer coefficient):

        IR ~= IC * sqrt(BR) * TC

    expected information ratio as a function of forecasting skill (IC),
    the number of independent bets (BR, see `effective_breadth`), and how
    well constraints let those bets reach the portfolio (TC, 1.0 = no
    constraint cost - the original, unconstrained form of the law).
    """
    return float(
        information_coefficient_value * np.sqrt(breadth_value) * transfer_coefficient_value
    )
