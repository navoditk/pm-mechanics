import cvxpy as cp
import numpy as np

from ._solver import check_optimal, solved_weights


def minimum_variance(covariance, long_only=True, max_weight=None):
    """Global minimum-variance weights: minimize w'Sigma*w s.t. sum(w)=1.

    max_weight is a uniform upper bound per asset. Note a long-only
    portfolio needs max_weight >= 1/n_assets to be feasible at all.
    """
    cov = np.asarray(covariance, float)
    n = cov.shape[0]
    w = cp.Variable(n)
    constraints = [cp.sum(w) == 1]
    if long_only:
        constraints.append(w >= 0)
    if max_weight is not None:
        constraints.append(w <= max_weight)
    problem = cp.Problem(cp.Minimize(cp.quad_form(w, cov)), constraints)
    return solved_weights(problem, w)


def mean_variance(expected_returns, covariance, risk_aversion=5.0, long_only=True, max_weight=None):
    """Mean-variance optimal weights under the standard utility

        maximize  mu'w - (risk_aversion / 2) * w'Sigma*w    s.t. sum(w) = 1

    The factor of 1/2 is the convention this repo uses throughout, and it
    matters: its first-order condition is `mu = risk_aversion * Sigma * w`,
    which is exactly what `pm.robust.market_implied_returns` inverts. Drop
    the 1/2 here and reverse-optimizing market weights into implied returns
    and back no longer round-trips (it closes at risk_aversion/2 instead).
    See `reference/concepts/mean_variance_optimization.md`.
    """
    mu = np.asarray(expected_returns, float)
    cov = np.asarray(covariance, float)
    n = len(mu)
    w = cp.Variable(n)
    constraints = [cp.sum(w) == 1]
    if long_only:
        constraints.append(w >= 0)
    if max_weight is not None:
        constraints.append(w <= max_weight)
    objective = cp.Maximize(mu @ w - 0.5 * risk_aversion * cp.quad_form(w, cov))
    return solved_weights(cp.Problem(objective, constraints), w)


def efficient_frontier(expected_returns, covariance, n_points=20, long_only=True):
    """Trace the efficient frontier: for `n_points` target returns spanning
    the achievable range (from the lowest- to highest-expected-return
    asset), solve the minimum-variance portfolio that hits each target.

    Returns (target_returns, volatilities, weights) - weights has shape
    (n_points, n_assets). Every point is on the frontier by construction,
    including the "inefficient" lower half below the global minimum-
    variance point - see reference/concepts/efficient_frontier.md for why
    that's a feature (it demonstrates domination), not a bug.
    """
    mu = np.asarray(expected_returns, float)
    cov = np.asarray(covariance, float)
    n = len(mu)
    targets = np.linspace(mu.min(), mu.max(), n_points)
    volatilities = np.zeros(n_points)
    weights = np.zeros((n_points, n))
    for i, target in enumerate(targets):
        w = cp.Variable(n)
        constraints = [cp.sum(w) == 1, mu @ w == target]
        if long_only:
            constraints.append(w >= 0)
        problem = cp.Problem(cp.Minimize(cp.quad_form(w, cov)), constraints)
        w_val = solved_weights(problem, w)
        weights[i] = w_val
        volatilities[i] = float(np.sqrt(w_val @ cov @ w_val))
    return targets, volatilities, weights


def max_sharpe(expected_returns, covariance, risk_free_rate=0.0, long_only=True):
    """Tangency portfolio: the weights that maximize the Sharpe ratio
    (mu'w - risk_free_rate) / sqrt(w'Sigma*w), s.t. sum(w) = 1.

    Maximizing a ratio isn't directly a convex problem, so:
    - long_only=False uses the closed form w ~ Sigma^-1 @ (mu - rf),
      renormalized to sum to 1 - the unconstrained tangency portfolio,
      independent of risk aversion.
    - long_only=True uses the standard change-of-variables reformulation
      (Cornuejols & Tutuncu): solve for y, kappa >= 0 with y >= 0,
      (mu-rf)'y = 1, sum(y) = kappa, minimizing y'Sigma*y, then divide
      w = y / kappa. This turns the fractional objective into a QP.

    Requires at least one asset with expected return above risk_free_rate
    - otherwise no long-only portfolio has a well-defined tangency point.
    """
    mu = np.asarray(expected_returns, float)
    cov = np.asarray(covariance, float)
    excess = mu - risk_free_rate
    if not np.any(excess > 0):
        raise ValueError(
            "At least one asset needs expected return above risk_free_rate "
            "for a tangency portfolio to exist."
        )

    if not long_only:
        raw = np.linalg.solve(cov, excess)
        return raw / raw.sum()

    n = len(mu)
    y = cp.Variable(n, nonneg=True)
    kappa = cp.Variable(nonneg=True)
    constraints = [excess @ y == 1, cp.sum(y) == kappa]
    problem = cp.Problem(cp.Minimize(cp.quad_form(y, cov)), constraints)
    check_optimal(problem)
    if y.value is None or kappa.value is None or kappa.value <= 1e-9:
        raise ValueError(
            "Tangency portfolio solve failed or is degenerate (kappa near "
            "zero) - check that expected_returns has meaningful excess "
            "return above risk_free_rate."
        )
    return np.asarray(y.value, dtype=float).ravel() / float(kappa.value)


def min_tracking_error(benchmark_weights, covariance, long_only=True, max_weight=None):
    """Portfolio weights minimizing tracking error to a benchmark:

        minimize  (w - w_b)'Sigma(w - w_b)    s.t. sum(w) = 1

    Holding the benchmark exactly (w = w_b) is always feasible and gives
    TE = 0, so - absent long_only/max_weight ruling it out - this always
    returns the benchmark's own weights. Real use is with active
    constraints layered in (see `pm.active.tracking_error` for measuring
    the result), e.g. a max_weight tighter than some benchmark position.
    """
    wb = np.asarray(benchmark_weights, float)
    cov = np.asarray(covariance, float)
    n = len(wb)
    w = cp.Variable(n)
    active = w - wb
    constraints = [cp.sum(w) == 1]
    if long_only:
        constraints.append(w >= 0)
    if max_weight is not None:
        constraints.append(w <= max_weight)
    problem = cp.Problem(cp.Minimize(cp.quad_form(active, cov)), constraints)
    return solved_weights(problem, w)
