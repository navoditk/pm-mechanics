import numpy as np


def total_attribution(contributions):
    return float(sum(contributions.values()))


def brinson_attribution(portfolio_weights, benchmark_weights, portfolio_returns, benchmark_returns):
    """Classic 3-effect Brinson decomposition per segment (sector, country,
    ...). allocation + selection + interaction sums to total active return.
    """
    wp = np.asarray(portfolio_weights, dtype=float)
    wb = np.asarray(benchmark_weights, dtype=float)
    rp = np.asarray(portfolio_returns, dtype=float)
    rb = np.asarray(benchmark_returns, dtype=float)
    allocation = (wp - wb) * rb
    selection = wb * (rp - rb)
    interaction = (wp - wb) * (rp - rb)
    return allocation, selection, interaction


def fixed_income_return_decomposition(carry, curve_effect, spread_effect):
    """Combine already-computed carry/curve/spread contributions (e.g. from
    key_rate_return_approximation and spread_pnl) into one reportable
    total - a labeling/reporting helper, not new math.
    """
    total = carry + curve_effect + spread_effect
    return {"carry": carry, "curve": curve_effect, "spread": spread_effect, "total": total}


def transaction_cost(trade_value, cost_bps):
    return abs(trade_value) * cost_bps / 10_000.0


def rebalancing_trades(current_weights, target_weights, portfolio_value):
    """Dollar trade needed per position to move from current to target
    weights. Positive = buy, negative = sell.
    """
    current = np.asarray(current_weights, dtype=float)
    target = np.asarray(target_weights, dtype=float)
    return (target - current) * portfolio_value
