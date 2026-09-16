from datetime import date

import numpy as np
import pytest

from pm.fixed_income.settlement import (
    accrued_interest,
    clean_price,
    day_count_fraction,
    dirty_price,
    invoice_amount,
)


def test_thirty_360_full_year_is_exactly_one():
    assert np.isclose(day_count_fraction(date(2024, 1, 15), date(2025, 1, 15), "30/360"), 1.0)


def test_thirty_360_treats_every_month_as_thirty_days():
    # Feb 15 -> Mar 15 is 28 actual days but 30 under 30/360.
    assert np.isclose(
        day_count_fraction(date(2023, 2, 15), date(2023, 3, 15), "30/360"), 30 / 360
    )


def test_thirty_360_collapses_a_31st_end_date_only_after_start_adjusts():
    # Start on a 31st adjusts to 30, which then lets the end 31st adjust too:
    # Jan 31 -> Mar 31 counts as 60 days, not 61.
    assert np.isclose(
        day_count_fraction(date(2024, 1, 31), date(2024, 3, 31), "30/360"), 60 / 360
    )
    # Start on a 30th, end on a 31st: end still collapses to 30.
    assert np.isclose(
        day_count_fraction(date(2024, 1, 30), date(2024, 3, 31), "30/360"), 60 / 360
    )
    # Start mid-month: the end 31st does NOT collapse, so Jan 15 -> Mar 31
    # is 30 + 16 = 76 days, not 75.
    assert np.isclose(
        day_count_fraction(date(2024, 1, 15), date(2024, 3, 31), "30/360"), 76 / 360
    )


def test_actual_conventions_use_real_elapsed_days():
    start, end = date(2024, 1, 1), date(2024, 3, 1)  # 60 actual days (leap year)
    assert np.isclose(day_count_fraction(start, end, "ACT/360"), 60 / 360)
    assert np.isclose(day_count_fraction(start, end, "ACT/365"), 60 / 365)


def test_act_act_uses_366_in_a_leap_year():
    start, end = date(2024, 1, 1), date(2024, 3, 1)
    assert np.isclose(day_count_fraction(start, end, "ACT/ACT"), 60 / 366)
    # Same calendar span in a non-leap year divides by 365 and spans 59 days.
    assert np.isclose(
        day_count_fraction(date(2023, 1, 1), date(2023, 3, 1), "ACT/ACT"), 59 / 365
    )


def test_the_convention_actually_changes_the_answer():
    # The whole reason a bond's day-count convention must be stated: the same
    # dates and the same coupon give materially different accrued interest.
    kwargs = {
        "face": 100.0,
        "coupon_rate": 0.05,
        "last_coupon_date": date(2024, 1, 1),
        "settlement_date": date(2024, 3, 1),
        "frequency": 2,
    }
    by_convention = {c: accrued_interest(convention=c, **kwargs) for c in
                     ("30/360", "ACT/360", "ACT/365", "ACT/ACT")}
    assert len(set(np.round(list(by_convention.values()), 10))) > 1


def test_accrued_is_zero_on_a_coupon_date_and_full_coupon_after_one_period():
    coupon_date = date(2024, 1, 1)
    assert np.isclose(
        accrued_interest(100.0, 0.06, coupon_date, coupon_date, 2, "30/360"), 0.0
    )
    # A full six-month period has accrued exactly one coupon.
    assert np.isclose(
        accrued_interest(100.0, 0.06, coupon_date, date(2024, 7, 1), 2, "30/360"), 3.0
    )


def test_accrued_is_half_a_coupon_at_the_period_midpoint():
    assert np.isclose(
        accrued_interest(100.0, 0.06, date(2024, 1, 1), date(2024, 4, 1), 2, "30/360"),
        1.5,
    )


def test_dirty_and_clean_price_round_trip():
    accrued = accrued_interest(100.0, 0.05, date(2024, 1, 1), date(2024, 3, 1))
    dirty = dirty_price(98.5, accrued)
    assert dirty > 98.5
    assert np.isclose(clean_price(dirty, accrued), 98.5)


def test_invoice_amount_scales_a_per_100_quote_to_face():
    # 1,000,000 face at 98.5 clean with 1.25 accrued settles at 997,500.
    assert np.isclose(invoice_amount(1_000_000, 98.5, 1.25), 997_500.0)


def test_unknown_convention_raises_rather_than_defaulting():
    with pytest.raises(ValueError, match="unknown day-count convention"):
        day_count_fraction(date(2024, 1, 1), date(2024, 2, 1), "ACT/366")


def test_reversed_dates_raise():
    with pytest.raises(ValueError, match="must not precede"):
        day_count_fraction(date(2024, 3, 1), date(2024, 1, 1))


def test_non_positive_frequency_raises():
    with pytest.raises(ValueError, match="frequency must be positive"):
        accrued_interest(100.0, 0.05, date(2024, 1, 1), date(2024, 3, 1), frequency=0)
