import math
from hypothesis import given, assume, strategies as st

def latency_rolling_avg(series, *, window=5, warmup_min=2):
    """
    Compute a moving average for latency.
    """
    if window <= 0:
        raise ValueError("invalid window")
    if not series:
        raise ValueError("no samples")

    tail = series[-window:]
    total = sum(tail)

    # BUG: ignores actual count during warmup.
    avg = total / window

    if len(tail) < warmup_min:
        return None
    return avg

@given(st.integers(max_value=0))  # Generator: integer with max value 0 (Branch: window <= 0)
def test_valid_window_negative(window):
    try:
        latency_rolling_avg([], window=window)
    except ValueError as e:
        assert str(e) == "invalid window"

@given(st.lists(st.integers(), max_size=0))  # Generator: empty list (Branch: not series)
def test_non_empty_series_empty(series):
    try:
        latency_rolling_avg(series)
    except ValueError as e:
        assert str(e) == "no samples"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=5), st.integers(min_value=0, max_value=4))  # Generator: list of floats with min size 5 and window less than warmup_min
def test_ignore_actual_count(tail, warmup_min):
    assume(len(tail) < warmup_min)
    assert latency_rolling_avg(tail, window=len(tail), warmup_min=warmup_min) is None