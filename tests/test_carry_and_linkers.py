import numpy as np

from pm.fixed_income.bond import bond_price
from pm.fixed_income.carry import carry_and_rolldown, carry_return, rolldown_return
from pm.fixed_income.curve import interpolate_zero_rate
from pm.fixed_income.duration import modified_duration
from pm.fixed_income.linkers import (
    breakeven_inflation,
    tips_coupon_payment,
    tips_index_ratio,
    tips_inflation_adjusted_principal,
)


def test_carry_return_matches_external_worked_example():
    # 5Y bond yielding 4.00% (at par), financed at 3.00% repo, held 1 year:
    # carry = (4.00% - 3.00%) * 1 = 1.00%.
    carry = carry_return(coupon_income=4.0, price=100.0, financing_rate=0.03, horizon_years=1.0)
    assert np.isclose(carry, 0.01)


def test_carry_return_negative_when_financing_exceeds_running_yield():
    carry = carry_return(coupon_income=4.0, price=100.0, financing_rate=0.05, horizon_years=1.0)
    assert carry < 0


def test_rolldown_return_positive_on_normal_upward_sloping_curve():
    # rolling to a lower yield (normal curve) should be a price GAIN
    rolldown = rolldown_return(modified_duration=4.5, current_yield=0.041, rolled_yield=0.038)
    assert rolldown > 0


def test_rolldown_return_negative_on_inverted_curve():
    # rolling to a HIGHER yield (inverted curve) should be a price LOSS
    rolldown = rolldown_return(modified_duration=4.5, current_yield=0.041, rolled_yield=0.042)
    assert rolldown < 0


def test_carry_and_rolldown_real_curve_example():
    # Same 4Y/5Y points as reference/fixed_income/carry_and_rolldown.md's
    # worked example, using this repo's own mock_curve.csv-style data
    # (locally inverted between 4Y and 5Y).
    tenors = [1, 2, 3, 4, 5, 10, 30]
    yields = [0.0480, 0.0450, 0.0430, 0.0420, 0.0410, 0.0400, 0.0410]
    y5 = interpolate_zero_rate(5, tenors, yields)
    y4 = interpolate_zero_rate(4, tenors, yields)

    price = bond_price(y5, face=100, coupon_rate=0.04, years=5, frequency=2)
    mod_dur = modified_duration(y5, face=100, coupon_rate=0.04, years=5, frequency=2)

    total = carry_and_rolldown(
        coupon_income=4.0,
        price=price,
        financing_rate=0.045,
        modified_duration=mod_dur,
        current_yield=y5,
        rolled_yield=y4,
        horizon_years=1.0,
    )
    # both legs are negative here (financing > running yield, curve
    # inverted at this segment) - the real lesson of this example
    assert total < 0
    carry = carry_return(4.0, price, 0.045, 1.0)
    rolldown = rolldown_return(mod_dur, y5, y4)
    assert np.isclose(total, carry + rolldown)


def test_breakeven_inflation_hand_example():
    # 10Y nominal 4.5%, 10Y TIPS (real) 2.0% -> breakeven 2.5%
    assert np.isclose(breakeven_inflation(0.045, 0.02), 0.025)


def test_tips_index_ratio_and_adjusted_principal():
    index_ratio = tips_index_ratio(cpi_reference_current=310.0, cpi_reference_base=300.0)
    assert np.isclose(index_ratio, 310 / 300)
    adjusted = tips_inflation_adjusted_principal(100.0, index_ratio)
    assert np.isclose(adjusted, 100.0 * 310 / 300)


def test_tips_index_ratio_of_one_leaves_principal_unchanged():
    index_ratio = tips_index_ratio(300.0, 300.0)
    assert np.isclose(index_ratio, 1.0)
    assert np.isclose(tips_inflation_adjusted_principal(100.0, index_ratio), 100.0)


def test_tips_coupon_payment_scales_with_inflation_adjusted_principal():
    # a 1% real coupon on an inflation-adjusted principal of $103.33,
    # paid semiannually: 0.01 * 103.33 / 2
    adjusted_principal = 103.33
    coupon = tips_coupon_payment(0.01, adjusted_principal, frequency=2)
    assert np.isclose(coupon, 0.01 * adjusted_principal / 2)


def test_tips_coupon_payment_higher_after_inflation_than_at_issuance():
    coupon_at_issuance = tips_coupon_payment(0.01, 100.0, frequency=2)
    coupon_after_inflation = tips_coupon_payment(0.01, 105.0, frequency=2)
    assert coupon_after_inflation > coupon_at_issuance
