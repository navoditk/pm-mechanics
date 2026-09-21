import numpy as np
import pytest

from pm.fixed_income.bond import bond_price
from pm.fixed_income.duration import modified_duration
from pm.fixed_income.mbs import (
    apply_prepayment,
    dollar_roll_implied_financing_rate,
    effective_duration,
    mortgage_amortization_schedule,
    psa_cpr,
    refinancing_incentive_cpr,
    single_monthly_mortality,
    weighted_average_life,
)


def test_amortization_schedule_fully_pays_off_balance():
    _, principal, _, ending = mortgage_amortization_schedule(1000.0, 0.12, 24)
    assert np.isclose(principal.sum(), 1000.0)
    assert np.isclose(ending[-1], 0.0, atol=1e-6)


def test_single_monthly_mortality_hand_example():
    expected = 1 - (1 - 0.06) ** (1 / 12)
    assert np.isclose(single_monthly_mortality(0.06), expected)


def test_psa_cpr_ramp_and_cap():
    assert np.isclose(psa_cpr(1), 0.002)
    assert np.isclose(psa_cpr(30), 0.06)
    assert np.isclose(psa_cpr(60), 0.06)
    assert np.isclose(psa_cpr(15, psa_multiplier=2.0), 0.06)


def test_psa_cpr_accepts_a_month_array():
    # apply_prepayment vectorizes smm over a whole schedule, so psa_cpr
    # needs to accept a month array too, not just a scalar.
    months = np.array([1, 10, 40])
    assert np.allclose(psa_cpr(months), [0.002, 0.02, 0.06])


def test_apply_prepayment_zero_smm_matches_scheduled():
    beginning = np.array([1000.0, 502.49])
    scheduled = np.array([497.51, 502.49])
    total, ending = apply_prepayment(beginning, scheduled, smm=0.0)
    assert np.allclose(total, scheduled)
    assert np.allclose(ending, beginning - scheduled)


def test_apply_prepayment_positive_smm_speeds_paydown():
    beginning = np.array([1000.0])
    scheduled = np.array([100.0])
    total, ending = apply_prepayment(beginning, scheduled, smm=0.10)
    assert np.isclose(total[0], 100.0 + (1000.0 - 100.0) * 0.10)
    assert np.isclose(ending[0], 1000.0 - total[0])


def test_refinancing_incentive_cpr_floors_at_base_when_no_incentive():
    assert np.isclose(refinancing_incentive_cpr(0.06, 0.08, base_cpr=0.06, sensitivity=2.0), 0.06)


def test_refinancing_incentive_cpr_rises_with_incentive():
    cpr = refinancing_incentive_cpr(0.06, 0.04, base_cpr=0.06, sensitivity=2.0)
    assert np.isclose(cpr, 0.06 + 2.0 * 0.02)


def test_weighted_average_life_hand_example():
    wal = weighted_average_life([1, 2, 3], [500, 300, 200])
    assert np.isclose(wal, 1.7)


def test_effective_duration_hand_example():
    ed = effective_duration(price_down=102.5, price_up=98.0, price_base=100.0, bump_decimal=0.0025)
    assert np.isclose(ed, 9.0)


def test_effective_duration_matches_modified_duration_for_plain_bond():
    ytm, face, coupon_rate, years, frequency = 0.05, 100.0, 0.05, 5.0, 2
    bump = 0.0001
    price_base = bond_price(ytm, face, coupon_rate, years, frequency)
    price_up = bond_price(ytm + bump, face, coupon_rate, years, frequency)
    price_down = bond_price(ytm - bump, face, coupon_rate, years, frequency)
    ed = effective_duration(price_down, price_up, price_base, bump)
    md = modified_duration(ytm, face, coupon_rate, years, frequency)
    assert np.isclose(ed, md, atol=1e-4)


def test_refinancing_incentive_cpr_caps_below_one():
    # An extreme incentive/sensitivity combination must stay a valid input
    # to single_monthly_mortality (cpr < 1), never reach or exceed 1 - at
    # cpr >= 1, single_monthly_mortality's (1-cpr)**(1/12) goes complex
    # instead of raising, which would silently corrupt a cash-flow schedule.
    cpr = refinancing_incentive_cpr(wac=0.10, market_rate=0.0, sensitivity=12.0)
    assert cpr < 1.0
    smm = single_monthly_mortality(cpr)
    assert np.isreal(smm)


def test_single_monthly_mortality_rejects_cpr_at_or_above_one():
    with pytest.raises(ValueError, match=r"\[0, 1\)"):
        single_monthly_mortality(1.0)


def test_amortization_schedule_handles_zero_rate():
    # r=0 makes the standard annuity-payment formula divide by zero
    # (1-(1+0)**-n == 0); a 0% loan should just amortize evenly.
    _, principal, interest, ending = mortgage_amortization_schedule(1200.0, 0.0, 12)
    assert np.allclose(principal, 100.0)
    assert np.allclose(interest, 0.0)
    assert np.isclose(ending[-1], 0.0)


def test_dollar_roll_implied_financing_rate_hand_example():
    # $1mm face, 5% coupon, near 101.00 / far 100.625 (0.375 drop), 1-month roll
    face, coupon_rate = 1_000_000.0, 0.05
    near_price, far_price = 101.00, 100.625
    coupon_income = face * coupon_rate / 12
    drop_income = (near_price - far_price) / 100 * face
    near_amount = near_price / 100 * face
    rate = dollar_roll_implied_financing_rate(
        coupon_income, drop_income, near_amount, horizon_years=1 / 12
    )
    assert np.isclose(rate, 0.004950495, atol=1e-6)


def test_dollar_roll_negative_when_drop_exceeds_coupon_given_up():
    # A drop rich enough to outweigh the forgone coupon makes the roll
    # cheaper than free - a negative implied financing rate.
    coupon_income = 4166.6667
    drop_income = 9000.0
    rate = dollar_roll_implied_financing_rate(
        coupon_income, drop_income, near_amount=1_010_000.0, horizon_years=1 / 12
    )
    assert rate < 0.0


def test_dollar_roll_zero_drop_equals_pure_forgone_coupon_cost():
    # No compensating drop: the implied financing rate is just the
    # annualized coupon carry given up, same as holding cost with no roll benefit.
    face, coupon_rate = 1_000_000.0, 0.05
    coupon_income = face * coupon_rate / 12
    near_amount = 1_010_000.0
    rate = dollar_roll_implied_financing_rate(
        coupon_income, drop_income=0.0, near_amount=near_amount, horizon_years=1 / 12
    )
    assert np.isclose(rate, coupon_income / near_amount * 12)


def test_wal_shortens_with_refinancing_incentive():
    wac, balance, months = 0.06, 1_000_000.0, 360
    beginning, scheduled, _, _ = mortgage_amortization_schedule(balance, wac, months)
    times = np.arange(1, months + 1) / 12

    def wal_at(market_rate):
        cpr = refinancing_incentive_cpr(wac, market_rate)
        smm = single_monthly_mortality(cpr)
        total_principal, _ = apply_prepayment(beginning, scheduled, smm)
        return weighted_average_life(times, total_principal)

    assert wal_at(0.04) < wal_at(0.08)
