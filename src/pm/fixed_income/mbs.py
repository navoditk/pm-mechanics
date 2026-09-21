import numpy as np


def mortgage_amortization_schedule(balance, annual_rate, months):
    """Level-payment (scheduled, no prepayment) amortization schedule.

    Returns (beginning_balance, scheduled_principal, interest, ending_balance),
    each an array of length `months`.
    """
    r = annual_rate / 12
    payment = balance / months if r == 0 else balance * r / (1 - (1 + r) ** (-months))
    beginning = np.zeros(months)
    principal = np.zeros(months)
    interest = np.zeros(months)
    bal = balance
    for m in range(months):
        beginning[m] = bal
        interest[m] = bal * r
        principal[m] = payment - interest[m]
        bal -= principal[m]
    ending = beginning - principal
    return beginning, principal, interest, ending


def single_monthly_mortality(cpr):
    """Convert an annualized CPR to a monthly prepayment rate (SMM).

    cpr must be in [0, 1) - at cpr=1, (1-cpr)**(1/12) is 0/0-adjacent and
    above 1 the base of the fractional power goes negative, which returns
    a complex number instead of raising. refinancing_incentive_cpr caps its
    output below 1 for exactly this reason.
    """
    cpr = np.asarray(cpr, dtype=float)
    if np.any(cpr < 0) or np.any(cpr >= 1):
        raise ValueError("cpr must be in [0, 1).")
    return 1 - (1 - cpr) ** (1 / 12)


def psa_cpr(month, psa_multiplier=1.0):
    """CPR implied by the PSA benchmark: ramps linearly from 0% to
    6%*psa_multiplier over the first 30 months, then flat.

    month may be a scalar or an array (np.minimum, not the builtin min,
    so this composes with apply_prepayment's vectorized month loop).
    """
    return 0.06 * psa_multiplier * np.minimum(month, 30) / 30


def apply_prepayment(beginning_balance, scheduled_principal, smm):
    """Overlay a prepayment assumption on a scheduled amortization.

    smm may be a scalar (constant) or an array matching beginning_balance.
    Returns (total_principal, ending_balance).
    """
    beginning_balance = np.asarray(beginning_balance, dtype=float)
    scheduled_principal = np.asarray(scheduled_principal, dtype=float)
    smm = np.broadcast_to(np.asarray(smm, dtype=float), beginning_balance.shape)
    prepay = (beginning_balance - scheduled_principal) * smm
    total_principal = scheduled_principal + prepay
    ending_balance = beginning_balance - total_principal
    return total_principal, ending_balance


def refinancing_incentive_cpr(wac, market_rate, base_cpr=0.06, sensitivity=2.0):
    """Simple behavioral prepayment model: CPR rises with refinancing
    incentive (wac - market_rate) when rates fall, and floors at base_cpr
    when rates rise (no incentive to refinance) - this asymmetry is the
    source of MBS negative convexity/extension risk.

    Capped just under 1.0 (a pool can't prepay more than 100%/year) so the
    result is always a valid input to single_monthly_mortality - uncapped,
    a large incentive/sensitivity combination produces a CPR >= 1 that
    turns single_monthly_mortality complex instead of raising.
    """
    incentive = np.maximum(0.0, wac - market_rate)
    return np.minimum(base_cpr + sensitivity * incentive, 0.999)


def weighted_average_life(times, principal_payments):
    times = np.asarray(times, dtype=float)
    principal_payments = np.asarray(principal_payments, dtype=float)
    return float(np.sum(times * principal_payments) / np.sum(principal_payments))


def effective_duration(price_down, price_up, price_base, bump_decimal):
    """Numerical (bump-and-reprice) duration - the right tool when price
    isn't a closed-form function of yield, e.g. because prepayment speed
    changes with rates. Contrast with modified_duration (closed-form).
    """
    return (price_down - price_up) / (2 * price_base * bump_decimal)


def dollar_roll_implied_financing_rate(coupon_income, drop_income, near_amount, horizon_years):
    """Annualized financing rate implied by a TBA dollar roll: sell MBS for
    near-month settlement, buy back (a substantially similar pool) for
    far-month settlement, giving up a month of coupon income in exchange
    for buying back at a lower ("dropped") price.

    implied_financing_rate = (coupon_income - drop_income) / near_amount / horizon_years

    coupon_income and drop_income are both dollar amounts over the roll
    period (not annualized); near_amount is the near-leg proceeds
    (near_price/100 * face); horizon_years is the roll period in years
    (a standard monthly TBA roll is ~1/12). If drop_income exceeds
    coupon_income the rate goes negative - the roll pays you more than the
    coupon you gave up, cheaper than any real financing rate. Compare
    against the prevailing GC repo rate: a dollar roll priced well below
    GC repo is "special" - see reference/fixed_income/tba_and_dollar_roll.md.
    This is a simplified version of the real calculation, which also nets
    reinvestment income on the sale proceeds and any principal paydown
    given up.
    """
    return (coupon_income - drop_income) / near_amount / horizon_years
