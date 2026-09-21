import numpy as np
from scipy.stats import norm


def portfolio_variance(weights, covariance):
    w = np.asarray(weights, dtype=float)
    cov = np.asarray(covariance, dtype=float)
    return float(w @ cov @ w)


def portfolio_volatility(weights, covariance):
    return portfolio_variance(weights, covariance) ** 0.5


def marginal_risk_contribution(weights, covariance):
    w = np.asarray(weights, dtype=float)
    cov = np.asarray(covariance, dtype=float)
    sigma = portfolio_volatility(w, cov)
    if sigma <= 0:
        raise ValueError("Portfolio volatility must be positive.")
    return (cov @ w) / sigma


def component_risk_contribution(weights, covariance):
    w = np.asarray(weights, dtype=float)
    return w * marginal_risk_contribution(w, covariance)


def group_risk_contribution(weights, covariance, groups):
    """Aggregate component_risk_contribution by group (sector, country,
    rating bucket, ...) - the risk decomposition a daily risk report
    actually shows, one row per group instead of one row per position.

    groups: a sequence with one label per asset, same length as weights
    (e.g. ["Tech", "Tech", "Energy", ...]). Returns {group: contribution},
    summing to the same total as sum(component_risk_contribution(...)).
    """
    contributions = component_risk_contribution(weights, covariance)
    groups = list(groups)
    if len(groups) != len(contributions):
        raise ValueError("groups must have exactly one label per asset (same length as weights).")
    totals = {}
    for group, contribution in zip(groups, contributions):
        totals[group] = totals.get(group, 0.0) + float(contribution)
    return totals


def parametric_var(portfolio_value, volatility, confidence=0.95):
    """Gaussian (delta-normal) VaR, same units/horizon as volatility."""
    z = norm.ppf(confidence)
    return portfolio_value * volatility * z


def expected_shortfall(portfolio_value, volatility, confidence=0.95):
    """Gaussian expected shortfall (average loss beyond the VaR threshold)."""
    z = norm.ppf(confidence)
    return portfolio_value * volatility * norm.pdf(z) / (1 - confidence)
