import numpy as np


def beta(stock_returns, market_returns):
    """OLS beta: Cov(stock, market) / Var(market)."""
    stock = np.asarray(stock_returns, dtype=float)
    market = np.asarray(market_returns, dtype=float)
    covariance = np.cov(stock, market, ddof=1)[0, 1]
    variance = np.var(market, ddof=1)
    return float(covariance / variance)


def equity_risk_premium(expected_market_return, risk_free_rate):
    return expected_market_return - risk_free_rate


def capm_expected_return(risk_free_rate, beta_value, equity_risk_premium_value):
    return risk_free_rate + beta_value * equity_risk_premium_value


def jensens_alpha(realized_return, risk_free_rate, beta_value, market_return):
    """Realized return in excess of what CAPM would have predicted -
    the standard risk-adjusted skill measure."""
    erp = equity_risk_premium(market_return, risk_free_rate)
    expected = capm_expected_return(risk_free_rate, beta_value, erp)
    return realized_return - expected
