import numpy as np

from pm.fixed_income.convertibles import conversion_premium, conversion_value
from pm.fixed_income.munis import tax_equivalent_yield


def test_tax_equivalent_yield_hand_example():
    # A 3% muni yield for an investor in a 32% marginal tax bracket.
    assert np.isclose(tax_equivalent_yield(muni_yield=0.03, tax_rate=0.32), 0.044117647, atol=1e-8)


def test_tax_equivalent_yield_zero_tax_rate_is_a_no_op():
    assert np.isclose(tax_equivalent_yield(muni_yield=0.04, tax_rate=0.0), 0.04)


def test_tax_equivalent_yield_rises_with_tax_rate():
    low = tax_equivalent_yield(0.03, tax_rate=0.20)
    high = tax_equivalent_yield(0.03, tax_rate=0.40)
    assert high > low


def test_conversion_value_hand_example():
    # A $1,000-par bond convertible into 20 shares, stock at $45.
    assert np.isclose(conversion_value(conversion_ratio=20, stock_price=45.0), 900.0)


def test_conversion_premium_hand_example():
    cv = conversion_value(conversion_ratio=20, stock_price=45.0)
    # Bond trades at 95 (price 950) against a 900 conversion value.
    assert np.isclose(conversion_premium(bond_price=950.0, conv_value=cv), 0.055555556, atol=1e-8)


def test_conversion_premium_zero_when_bond_trades_at_conversion_value():
    cv = conversion_value(conversion_ratio=20, stock_price=47.5)
    assert np.isclose(conversion_premium(bond_price=950.0, conv_value=cv), 0.0, atol=1e-8)


def test_conversion_value_scales_linearly_with_stock_price():
    low = conversion_value(conversion_ratio=20, stock_price=40.0)
    high = conversion_value(conversion_ratio=20, stock_price=80.0)
    assert np.isclose(high, 2 * low)
