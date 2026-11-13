"""csTimer-style averages computed from stored milliseconds.

Effective time: OK = t, +2 = t + 2000, DNF = infinity. AoN trims ceil(5% * N) from
each end (1 for Ao5 and Ao12, 5 for Ao100). Fewer than N solves gives None.
"""
import math

DNF = math.inf


def effective(time_ms: int, penalty: int) -> float:
    return DNF if penalty == 2 else time_ms + (2000 if penalty == 1 else 0)


def average_of(times, n: int):
    """Average of the last n effective times; None if undefined, DNF if too many DNFs."""
    if len(times) < n:
        return None
    window = sorted(times[-n:])
    cut = math.ceil(0.05 * n)
    kept = window[cut:n - cut]
    if kept[-1] == DNF:
        return DNF
    return round(sum(kept) / (10 * len(kept))) * 10  # rounded to centiseconds, in ms


def summary(times):
    finite = [t for t in times if t != DNF]
    return {
        "count": len(times),
        "best": min(finite) if finite else None,
        "mean": round(sum(finite) / len(finite)) if finite else None,
        "ao5": average_of(times, 5),
        "ao12": average_of(times, 12),
        "ao100": average_of(times, 100),
    }


def rolling(times, n: int):
    return [average_of(times[:i + 1], n) for i in range(len(times))]
