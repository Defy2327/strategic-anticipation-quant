"""Selected original implementation functions; not the final research pipeline.
See PROVENANCE.json for exact source locations. Function bodies are unchanged.
"""

import numpy as np


def decimal_cents(values: list[str]) -> np.ndarray:
    """Parse exact vendor decimal cents, with no float rounding or tolerance."""
    result = []
    for value in values:
        whole, separator, fraction = str(value).partition(".")
        assert whole.isdigit() and separator == "." and fraction.isdigit()
        assert 1 <= len(fraction) <= 2, "Unexpected precision: do not silently round"
        result.append(int(whole) * 100 + int(fraction.ljust(2, "0")))
    return np.array(result, dtype=np.int64)



def exact_live_geometry(
    cents: np.ndarray, prior_cents: np.ndarray, window: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Algebraically exact sign of P/M−1; integer numerator, positive denominator."""
    cents = np.asarray(cents, np.int64)
    prior = np.asarray(prior_cents, np.int64)
    assert (cents > 0).all() and len(prior) >= window - 1 and (prior > 0).all()
    total = prior[-(window - 1) :].sum(dtype=np.int64)
    numerator = (window - 1) * cents - total
    denominator = cents + total
    reference = denominator / (100 * window)
    distance = numerator / denominator
    crossing = np.flatnonzero((numerator[:-2] > 0) & (numerator[1:-1] <= 0)) + 1
    return reference, distance, crossing

