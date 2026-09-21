import numpy as np


def factor_model_covariance(exposures, factor_covariance, specific_variance):
    B = np.asarray(exposures, float)
    F = np.asarray(factor_covariance, float)
    d = np.asarray(specific_variance, float)
    return B @ F @ B.T + np.diag(d)


def portfolio_factor_exposure(weights, exposures):
    w = np.asarray(weights, float)
    B = np.asarray(exposures, float)
    return w @ B


def factor_variance_contribution(weights, exposures, factor_covariance):
    exposure = portfolio_factor_exposure(weights, exposures)
    F = np.asarray(factor_covariance, float)
    return float(exposure @ F @ exposure)


def specific_variance_contribution(weights, specific_variance):
    w = np.asarray(weights, float)
    d = np.asarray(specific_variance, float)
    return float(np.sum(w**2 * d))
