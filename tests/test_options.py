import numpy as np

from pm.options import (
    black76_call_price,
    black76_put_price,
    black_scholes_call_price,
    black_scholes_put_price,
    delta_call,
    delta_put,
    gamma,
    implied_volatility_call,
    implied_volatility_put,
    put_call_parity_residual,
    rho_call,
    rho_put,
    theta_call,
    theta_put,
    vega,
)

# Classic Hull textbook ATM example: S=K=100, r=5%, sigma=20%, T=1, q=0
S, K, R, SIGMA, T = 100.0, 100.0, 0.05, 0.20, 1.0


def test_black_scholes_call_hand_example():
    assert np.isclose(black_scholes_call_price(S, K, R, SIGMA, T), 10.450584, atol=1e-5)


def test_black_scholes_put_hand_example():
    assert np.isclose(black_scholes_put_price(S, K, R, SIGMA, T), 5.573526, atol=1e-5)


def test_put_call_parity_holds_for_consistent_bs_prices():
    call = black_scholes_call_price(S, K, R, SIGMA, T)
    put = black_scholes_put_price(S, K, R, SIGMA, T)
    assert np.isclose(put_call_parity_residual(call, put, S, K, R, T), 0.0, atol=1e-8)


def test_put_call_parity_residual_nonzero_for_inconsistent_quotes():
    # An arbitrary, non-BS-consistent call/put pair should NOT satisfy parity.
    residual = put_call_parity_residual(
        call_price=11.0, put_price=5.0, spot=S, strike=K, rate=R, time_to_expiry=T
    )
    assert not np.isclose(residual, 0.0, atol=1e-6)


def test_delta_call_and_delta_put_hand_example():
    assert np.isclose(delta_call(S, K, R, SIGMA, T), 0.636831, atol=1e-5)
    assert np.isclose(delta_put(S, K, R, SIGMA, T), -0.363169, atol=1e-5)


def test_delta_put_call_relationship():
    # delta_call - delta_put == exp(-qT); with q=0 that's exactly 1.0.
    assert np.isclose(delta_call(S, K, R, SIGMA, T) - delta_put(S, K, R, SIGMA, T), 1.0, atol=1e-8)


def test_gamma_matches_finite_difference():
    eps = 1e-3
    fd = (
        black_scholes_call_price(S + eps, K, R, SIGMA, T)
        - 2 * black_scholes_call_price(S, K, R, SIGMA, T)
        + black_scholes_call_price(S - eps, K, R, SIGMA, T)
    ) / eps**2
    assert np.isclose(gamma(S, K, R, SIGMA, T), fd, atol=1e-3)


def test_vega_matches_finite_difference():
    eps = 1e-4
    fd = (
        black_scholes_call_price(S, K, R, SIGMA + eps, T)
        - black_scholes_call_price(S, K, R, SIGMA - eps, T)
    ) / (2 * eps)
    assert np.isclose(vega(S, K, R, SIGMA, T), fd, atol=1e-4)


def test_vega_identical_for_call_and_put():
    # Vega is the same for a call and a put at the same strike/expiry - a
    # direct consequence of put-call parity (their difference, S - K*disc,
    # has zero vega).
    eps = 1e-4
    fd_put = (
        black_scholes_put_price(S, K, R, SIGMA + eps, T)
        - black_scholes_put_price(S, K, R, SIGMA - eps, T)
    ) / (2 * eps)
    assert np.isclose(vega(S, K, R, SIGMA, T), fd_put, atol=1e-4)


def test_theta_call_matches_finite_difference():
    eps = 1e-4
    fd = -(
        black_scholes_call_price(S, K, R, SIGMA, T + eps)
        - black_scholes_call_price(S, K, R, SIGMA, T - eps)
    ) / (2 * eps)
    assert np.isclose(theta_call(S, K, R, SIGMA, T), fd, atol=1e-3)


def test_theta_put_matches_finite_difference():
    eps = 1e-4
    fd = -(
        black_scholes_put_price(S, K, R, SIGMA, T + eps)
        - black_scholes_put_price(S, K, R, SIGMA, T - eps)
    ) / (2 * eps)
    assert np.isclose(theta_put(S, K, R, SIGMA, T), fd, atol=1e-3)


def test_rho_call_matches_finite_difference():
    eps = 1e-4
    fd = (
        black_scholes_call_price(S, K, R + eps, SIGMA, T)
        - black_scholes_call_price(S, K, R - eps, SIGMA, T)
    ) / (2 * eps)
    assert np.isclose(rho_call(S, K, R, SIGMA, T), fd, atol=1e-3)


def test_rho_put_matches_finite_difference():
    eps = 1e-4
    fd = (
        black_scholes_put_price(S, K, R + eps, SIGMA, T)
        - black_scholes_put_price(S, K, R - eps, SIGMA, T)
    ) / (2 * eps)
    assert np.isclose(rho_put(S, K, R, SIGMA, T), fd, atol=1e-3)


def test_theta_is_negative_for_atm_call_and_put():
    # Time decay: an ATM option loses value as expiry approaches, all else fixed.
    assert theta_call(S, K, R, SIGMA, T) < 0
    assert theta_put(S, K, R, SIGMA, T) < 0


def test_implied_volatility_call_round_trips():
    market_price = black_scholes_call_price(S, K, R, SIGMA, T)
    iv = implied_volatility_call(market_price, S, K, R, T)
    assert np.isclose(iv, SIGMA, atol=1e-8)


def test_implied_volatility_put_round_trips():
    market_price = black_scholes_put_price(S, K, R, SIGMA, T)
    iv = implied_volatility_put(market_price, S, K, R, T)
    assert np.isclose(iv, SIGMA, atol=1e-8)


def test_black76_matches_black_scholes_at_the_matching_forward():
    # Black-76 priced off the forward F = S*exp((r-q)T) must reproduce the
    # spot-based Black-Scholes price exactly - they're the same model.
    q = 0.0
    forward = S * np.exp((R - q) * T)
    assert np.isclose(
        black76_call_price(forward, K, R, SIGMA, T),
        black_scholes_call_price(S, K, R, SIGMA, T),
        atol=1e-8,
    )
    assert np.isclose(
        black76_put_price(forward, K, R, SIGMA, T),
        black_scholes_put_price(S, K, R, SIGMA, T),
        atol=1e-8,
    )


def test_call_price_increases_with_volatility():
    low = black_scholes_call_price(S, K, R, 0.10, T)
    high = black_scholes_call_price(S, K, R, 0.40, T)
    assert high > low
