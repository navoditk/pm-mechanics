def roll_yield(near_price, far_price):
    """Return from rolling a futures position from the near contract into
    the far contract. Positive in backwardation, negative in contango.
    """
    return (near_price - far_price) / far_price


def commodity_curve_state(near_price, far_price):
    if near_price > far_price:
        return "backwardation"
    if near_price < far_price:
        return "contango"
    return "flat"
