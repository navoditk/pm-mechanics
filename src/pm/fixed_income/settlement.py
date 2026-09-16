"""Settlement mechanics: what a bond buyer actually pays.

Every other module here works in clean prices - the quoted number. This one
covers the gap between that quote and the cash that changes hands, which is
where day-count conventions and accrued interest live.
"""

SUPPORTED_CONVENTIONS = ("30/360", "ACT/360", "ACT/365", "ACT/ACT")


def _thirty_360_days(start, end):
    """Day count under the 30/360 (US/NASD) convention, which pretends every
    month has 30 days and every year 360. Both end-of-month adjustments
    matter: a 31st collapses to a 30th, and only after the start date has
    been adjusted first (order is load-bearing - adjusting the end date
    first gives a different answer when both fall on a 31st).
    """
    d1, d2 = start.day, end.day
    if d1 == 31:
        d1 = 30
    if d2 == 31 and d1 == 30:
        d2 = 30
    return 360 * (end.year - start.year) + 30 * (end.month - start.month) + (d2 - d1)


def day_count_fraction(start, end, convention="30/360"):
    """Year-fraction between two dates under a stated day-count convention.

    The same coupon rate and the same two dates produce different accrued
    interest under different conventions, so the convention is never
    optional - it is part of the instrument's terms. ACT/ACT here is the
    simple ACT/ACT(ISDA)-style approximation that divides actual days by
    365 or 366 depending on whether the *end* year is a leap year; real
    ISDA ACT/ACT splits the period across year boundaries, which matters
    for periods spanning a year end.

    Returns a fraction of a year. Raises on an unknown convention rather
    than silently defaulting, because a wrong convention is a wrong number.
    """
    if convention not in SUPPORTED_CONVENTIONS:
        raise ValueError(
            f"unknown day-count convention {convention!r}; "
            f"supported: {', '.join(SUPPORTED_CONVENTIONS)}"
        )
    if end < start:
        raise ValueError("end date must not precede start date")
    if convention == "30/360":
        return _thirty_360_days(start, end) / 360.0
    actual_days = (end - start).days
    if convention == "ACT/360":
        return actual_days / 360.0
    if convention == "ACT/365":
        return actual_days / 365.0
    days_in_year = 366 if _is_leap(end.year) else 365
    return actual_days / days_in_year


def _is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def accrued_interest(
    face,
    coupon_rate,
    last_coupon_date,
    settlement_date,
    frequency=2,
    convention="30/360",
):
    """Interest earned by the seller since the last coupon but not yet paid.

    The buyer compensates the seller for it at settlement, because the buyer
    will receive the whole next coupon despite having held the bond for only
    part of the period.

    accrued = face * coupon_rate / frequency
              * (accrual fraction / full period fraction)

    Both fractions use the same convention, so the ratio is the share of the
    coupon period that has elapsed.
    """
    if frequency <= 0:
        raise ValueError("frequency must be positive")
    period_years = 1.0 / frequency
    elapsed = day_count_fraction(last_coupon_date, settlement_date, convention)
    coupon = face * coupon_rate / frequency
    return coupon * (elapsed / period_years)


def dirty_price(clean_price, accrued):
    """The full (invoice) price actually paid: quote plus accrued interest."""
    return clean_price + accrued


def clean_price(dirty, accrued):
    """The quoted price, recovered from the invoice price."""
    return dirty - accrued


def invoice_amount(face, clean_price_per_100, accrued):
    """Cash settlement amount for a position, scaled from a per-100 quote.

    Bond prices are quoted per 100 of face, so a 1,000,000 face position at
    a clean price of 98.5 with 1.25 accrued settles at
    1,000,000 / 100 * (98.5 + 1.25).
    """
    return face / 100.0 * dirty_price(clean_price_per_100, accrued)
