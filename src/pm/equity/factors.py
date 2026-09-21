import numpy as np


def active_share(portfolio_weights, benchmark_weights):
    """Half the sum of absolute active weights - the fraction of the
    portfolio, by market value, positioned differently from the benchmark.
    """
    wp = np.asarray(portfolio_weights, dtype=float)
    wb = np.asarray(benchmark_weights, dtype=float)
    return float(0.5 * np.sum(np.abs(wp - wb)))


def style_tilt(portfolio_exposure, benchmark_exposure):
    """Active exposure to a style factor (value, momentum, quality, size,
    low-vol, ...) versus the benchmark. Compute each side's exposure first
    with pm.factors.portfolio_factor_exposure(weights, factor_scores).
    """
    return portfolio_exposure - benchmark_exposure
