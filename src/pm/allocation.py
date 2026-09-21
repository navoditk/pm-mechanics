def funded_ratio(assets, liabilities):
    """Plan assets as a fraction of plan liabilities - the core metric a
    liability-driven investing (LDI) program manages. 1.0 = exactly
    funded; below 1.0 = underfunded. See
    reference/concepts/liability_driven_investing.md.
    """
    return assets / liabilities


def surplus(assets, liabilities):
    """Plan assets minus plan liabilities, in currency terms - the
    absolute counterpart to funded_ratio's ratio framing. Positive =
    overfunded, negative = underfunded (a deficit).
    """
    return assets - liabilities
