import numpy as np

from pm.fixed_income.bond import bond_cashflows, bond_price
from pm.fixed_income.credit import (
    cds_bond_basis,
    credit_spread_from_hazard,
    expected_loss,
    fixed_charge_coverage_ratio,
    index_basis,
    index_intrinsic_spread,
    interest_coverage_ratio,
    leverage_ratio,
    spread_pnl,
    survival_probability,
    z_spread,
)
from pm.fixed_income.curve import (
    bootstrap_zero_rates,
    forward_rate,
    interpolate_zero_rate,
    key_rate_return_approximation,
)
from pm.fixed_income.duration import convexity, dv01, hedge_ratio, macaulay_duration
from pm.fixed_income.futures import futures_dv01_per_contract
from pm.fixed_income.swaps import swap_dv01, swap_spread


def test_par_bond_at_coupon_yield():
    assert np.isclose(bond_price(0.05, face=100, coupon_rate=0.05, years=5, frequency=2), 100.0)


def test_bond_cashflows_hand_example():
    times, flows = bond_cashflows(face=100, coupon_rate=0.05, years=2, frequency=2)
    assert np.allclose(times, [0.5, 1.0, 1.5, 2.0])
    assert np.allclose(flows, [2.5, 2.5, 2.5, 102.5])


def test_key_rate_return_approximation_hand_example():
    r = key_rate_return_approximation([3, 5], [0.01, -0.005])
    assert np.isclose(r, -(3 * 0.01 + 5 * (-0.005)))


def test_dv01_positive():
    assert dv01(0.05, face=100, coupon_rate=0.05, years=5, frequency=2) > 0


def test_macaulay_duration_par_bond_hand_bound():
    # for a par bond, Macaulay duration must be less than its maturity
    # (coupons are received before the final principal payment)
    mac = macaulay_duration(0.05, face=100, coupon_rate=0.05, years=5, frequency=2)
    assert 0 < mac < 5


def test_convexity_matches_finite_difference_second_derivative():
    ytm, face, coupon_rate, years, frequency = 0.05, 100.0, 0.05, 5.0, 2
    h = 1e-4
    price_base = bond_price(ytm, face, coupon_rate, years, frequency)
    price_up = bond_price(ytm + h, face, coupon_rate, years, frequency)
    price_down = bond_price(ytm - h, face, coupon_rate, years, frequency)
    convexity_fd = (price_up - 2 * price_base + price_down) / h**2 / price_base

    c = convexity(ytm, face, coupon_rate, years, frequency)
    assert np.isclose(c, convexity_fd, rtol=1e-3)


def test_convexity_improves_on_duration_only_approximation():
    ytm, face, coupon_rate, years, frequency = 0.05, 100.0, 0.05, 5.0, 2
    dy = 0.02
    price_base = bond_price(ytm, face, coupon_rate, years, frequency)
    actual_return = bond_price(ytm + dy, face, coupon_rate, years, frequency) / price_base - 1

    d = macaulay_duration(ytm, face, coupon_rate, years, frequency) / (1 + ytm / frequency)
    c = convexity(ytm, face, coupon_rate, years, frequency)
    duration_only = -d * dy
    duration_plus_convexity = -d * dy + 0.5 * c * dy**2

    assert abs(duration_plus_convexity - actual_return) < abs(duration_only - actual_return)


def test_spread_widening_loses_money():
    assert spread_pnl(1_000_000, 4.0, 50) < 0


def test_interpolate_zero_rate_linear():
    assert np.isclose(interpolate_zero_rate(6, [2, 10], [0.03, 0.04]), 0.035)


def test_forward_rate_hand_example():
    expected = (1.03**2 / 1.02**1) ** (1 / (2 - 1)) - 1
    assert np.isclose(forward_rate(1, 0.02, 2, 0.03), expected)


def test_bootstrap_zero_rates_single_period_equals_par_yield():
    zero_rates = bootstrap_zero_rates([0.05])
    assert np.isclose(zero_rates[0], 0.05)


def test_bootstrap_zero_rates_two_period():
    zero_rates = bootstrap_zero_rates([0.05, 0.06])
    pv_first_coupon = 6 / 1.05
    expected_z2 = ((106) / (100 - pv_first_coupon)) ** (1 / 2) - 1
    assert np.isclose(zero_rates[1], expected_z2)


def test_hedge_ratio_short_to_offset_long_dv01():
    assert np.isclose(hedge_ratio(100_000, 50), -2000)


def test_swap_dv01_matches_par_bond_proxy():
    expected = dv01(0.04, face=10_000_000, coupon_rate=0.04, years=5, frequency=2)
    assert np.isclose(swap_dv01(10_000_000, 0.04, 5, 2), expected)


def test_swap_spread_and_futures_dv01():
    assert np.isclose(swap_spread(0.045, 0.040), 0.005)
    assert np.isclose(futures_dv01_per_contract(120, 0.9), 120 / 0.9)


def test_z_spread_matches_flat_curve_closed_form():
    par_price = bond_price(0.06, face=100, coupon_rate=0.06, years=5, frequency=2)
    spread = z_spread(
        par_price,
        face=100,
        coupon_rate=0.06,
        years=5,
        frequency=2,
        curve_tenors=[1, 30],
        curve_rates=[0.04, 0.04],
    )
    assert np.isclose(spread, 0.02, atol=1e-6)


def test_survival_probability_decreases_with_time():
    assert survival_probability(0.02, 0) == 1.0
    assert survival_probability(0.02, 5) < survival_probability(0.02, 1)


def test_expected_loss_hand_example():
    assert np.isclose(expected_loss(1_000_000, 0.02, 0.40), 12_000)


def test_credit_spread_from_hazard_hand_example():
    assert np.isclose(credit_spread_from_hazard(0.03, 0.40), 0.018)


def test_cds_bond_basis_hand_example():
    assert np.isclose(cds_bond_basis(0.018, 0.022), -0.004)


def test_leverage_ratio_hand_example():
    assert np.isclose(leverage_ratio(total_debt=300, ebitda=100), 3.0)


def test_interest_coverage_ratio_hand_example():
    assert np.isclose(interest_coverage_ratio(ebitda=100, interest_expense=20), 5.0)


def test_fixed_charge_coverage_is_stricter_than_interest_coverage():
    ebitda, interest = 100, 20
    coverage = interest_coverage_ratio(ebitda, interest)
    fixed_charge = fixed_charge_coverage_ratio(ebitda, interest, mandatory_principal_payments=10)
    assert np.isclose(fixed_charge, 100 / 30)
    assert fixed_charge < coverage


def test_fixed_charge_coverage_equals_interest_coverage_with_no_amortization():
    ebitda, interest = 100, 20
    assert np.isclose(
        fixed_charge_coverage_ratio(ebitda, interest, mandatory_principal_payments=0),
        interest_coverage_ratio(ebitda, interest),
    )


def test_index_intrinsic_spread_equal_weighted_hand_example():
    spreads = [80, 90, 100, 70, 110]
    assert np.isclose(index_intrinsic_spread(spreads), 90.0)


def test_index_intrinsic_spread_with_explicit_weights():
    spreads = [80, 90, 100, 70, 110]
    weights = [0.1, 0.2, 0.3, 0.2, 0.2]
    expected = sum(s * w for s, w in zip(spreads, weights))
    assert np.isclose(index_intrinsic_spread(spreads, weights=weights), expected)


def test_index_basis_hand_example():
    assert np.isclose(index_basis(index_spread=95, intrinsic_spread=90), 5)


def test_index_basis_zero_when_index_equals_intrinsic():
    assert np.isclose(index_basis(90, 90), 0.0)
