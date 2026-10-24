"""Selected original implementation functions; not the final research pipeline.
See PROVENANCE.json for exact source locations. Function bodies are unchanged.
"""

import numpy as np

MINUTE_NS = 60_000_000_000


def session_minutes(
    times_ns: np.ndarray, opens_ns: np.ndarray, closes_ns: np.ndarray
) -> np.ndarray:
    """Elapsed minutes of close-stamped events; first close is minute one."""
    times, opens, closes = [np.asarray(x, dtype=np.int64) for x in [times_ns, opens_ns, closes_ns]]
    if times.shape != opens.shape or times.shape != closes.shape:
        raise ValueError("One official open/close required per timestamp")
    elapsed, duration = times - opens, closes - opens
    if np.any(duration <= 120 * MINUTE_NS) or np.any(duration % MINUTE_NS):
        raise ValueError("Unsupported session duration")
    if np.any(elapsed <= 0) or np.any(elapsed > duration) or np.any(elapsed % MINUTE_NS):
        raise ValueError("Timestamp must be an exact same-session minute close")
    return elapsed // MINUTE_NS



def clock_regions(minutes: np.ndarray, length: np.ndarray) -> np.ndarray:
    """First/final 60 closing timestamps; session-length-aware disjoint regions."""
    minutes, length = np.asarray(minutes), np.asarray(length)
    if minutes.shape != length.shape or np.any(length <= 120):
        raise ValueError("Invalid session lengths")
    if np.any(minutes <= 0) or np.any(minutes > length):
        raise ValueError("Invalid session minute")
    return np.where(minutes <= 60, "OPEN", np.where(minutes > length - 60, "CLOSE", "MIDDAY"))

