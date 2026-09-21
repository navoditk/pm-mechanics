import cvxpy as cp
import numpy as np

from ._solver import solved_weights


def shrink_covariance(sample_covariance, shrinkage):
    """Shrink the sample covariance toward a diagonal target (correlations
    shrunk to zero, variances preserved). shrinkage in [0, 1]: 0 = sample
    covariance unchanged, 1 = fully diagonal.
    """
    cov = np.asarray(sample_covariance, dtype=float)
    target = np.diag(np.diag(cov))
    return shrinkage * target + (1 - shrinkage) * cov


def market_implied_returns(risk_aversion, covariance, market_weights):
    """Reverse-optimize the market-implied (equilibrium) expected returns
    that would make market_weights optimal - the Black-Litterman prior.

    `pi = risk_aversion * Sigma * w_market` is the first-order condition of
    `maximize mu'w - (risk_aversion / 2) * w'Sigma*w`, so this inverts
    `pm.optimization.mean_variance` exactly: feeding this pi back in at the
    same risk_aversion returns market_weights. That round trip is asserted
    in tests/test_robust.py and is the reason mean_variance carries the 1/2.
    """
    cov = np.asarray(covariance, dtype=float)
    w = np.asarray(market_weights, dtype=float)
    return risk_aversion * cov @ w


def black_litterman_posterior(
    prior_returns, covariance, view_matrix, view_returns, view_uncertainty, tau=0.05
):
    """Combine a prior (e.g. from market_implied_returns) with investor
    views (P, Q, Omega) into posterior expected returns and covariance.

    view_matrix (P): (k views x n assets) exposure of each view to assets.
    view_returns (Q): (k,) expected return of each view.
    view_uncertainty (Omega): (k x k) confidence in each view (covariance
    of view errors - smaller = more confident).

    Returns (posterior_mean, M) where M is the covariance of the *estimated
    mean*, not the posterior covariance of returns. If you feed a covariance
    into an optimizer after this, use `covariance + M` (or just `covariance`),
    never M alone - M is smaller by roughly a factor of tau and would make
    the optimizer wildly overconfident.
    """
    prior = np.asarray(prior_returns, dtype=float)
    sigma = np.asarray(covariance, dtype=float)
    P = np.asarray(view_matrix, dtype=float)
    Q = np.asarray(view_returns, dtype=float)
    omega = np.asarray(view_uncertainty, dtype=float)

    tau_sigma_inv = np.linalg.inv(tau * sigma)
    omega_inv = np.linalg.inv(omega)
    posterior_cov_inv = tau_sigma_inv + P.T @ omega_inv @ P
    posterior_cov = np.linalg.inv(posterior_cov_inv)
    posterior_mean = posterior_cov @ (tau_sigma_inv @ prior + P.T @ omega_inv @ Q)
    return posterior_mean, posterior_cov


def risk_parity_weights(covariance):
    """Long-only weights giving each asset equal risk contribution, via the
    standard convex reformulation (Maillard, Roncalli, Teiletche 2010):
    minimize 0.5*w'*Sigma*w - sum(log(w)), then renormalize to sum to 1.
    """
    cov = np.asarray(covariance, dtype=float)
    n = cov.shape[0]
    w = cp.Variable(n, pos=True)
    objective = cp.Minimize(0.5 * cp.quad_form(w, cov) - cp.sum(cp.log(w)))
    raw = solved_weights(cp.Problem(objective), w)
    return raw / raw.sum()


def scenario_robust_weights(scenario_returns, long_only=True):
    """Minimax (robust) portfolio: maximize the worst-case return across a
    given set of scenarios. scenario_returns is (n_scenarios x n_assets).
    """
    R = np.asarray(scenario_returns, dtype=float)
    n_assets = R.shape[1]
    w = cp.Variable(n_assets)
    t = cp.Variable()
    constraints = [cp.sum(w) == 1, R @ w >= t]
    if long_only:
        constraints.append(w >= 0)
    return solved_weights(cp.Problem(cp.Maximize(t), constraints), w)
