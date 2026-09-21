"""Shared private helpers - not part of the public pm API or agent tool
catalog (see scripts/generate_tool_schema.py's leading-underscore filter).
"""

import numpy as np


def finite_array(values, min_size=1):
    """Drop non-finite entries and return a float array.

    Return series built with `pm.returns.simple_returns`/`log_returns`
    carry a leading NaN by construction, so every metric that consumes a
    return series needs this. Without it, one NaN silently turns an
    entire ratio/statistic into NaN - and a `<= 0` guard downstream won't
    catch it, since `nan <= 0` is False.
    """
    arr = np.asarray(values, dtype=float)
    finite = arr[np.isfinite(arr)]
    if finite.size < min_size:
        raise ValueError(f"Need at least {min_size} finite observation(s); got {finite.size}.")
    return finite
