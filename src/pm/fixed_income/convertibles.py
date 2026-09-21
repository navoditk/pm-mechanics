def conversion_value(conversion_ratio, stock_price):
    """The convertible bond's value if converted into stock immediately
    (also called parity): conversion_ratio * stock_price.
    """
    return conversion_ratio * stock_price


def conversion_premium(bond_price, conv_value):
    """How much richer the convertible trades than its immediate
    conversion value, as a fraction: (bond_price - conv_value) / conv_value.

    This is a simplified version of the CFA-standard definition, which
    compares bond_price against max(conversion_value, straight_bond_value)
    rather than conversion_value alone - see
    reference/fixed_income/convertible_bonds.md for why the straight-bond
    floor isn't modeled here.
    """
    return (bond_price - conv_value) / conv_value
