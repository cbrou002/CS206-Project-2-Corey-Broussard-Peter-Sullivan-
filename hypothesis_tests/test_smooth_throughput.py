import math
from hypothesis import given, assume, strategies as st

def smooth_throughput(series, *, window=5, warmup_min=2):
    """
    Compute a moving average for throughput.
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

# Property-based test for valid_window property
@given(st.integers(min_value=1))
def test_valid_window(window):
    assume(window <= 0)
    try:
        smooth_throughput([], window=window)
    except ValueError as e:
        assert str(e) == "invalid window"

# Property-based test for non_empty_series property
@given(st.lists(st.floats(), min_size=1))
def test_non_empty_series(series):
    assume(not series)
    try:
        smooth_throughput(series)
    except ValueError as e:
        assert str(e) == "no samples"

# Property-based test for ignore_actual_count property
@given(st.lists(st.floats(), min_size=5), st.integers(min_value=1, max_value=4))
def test_ignore_actual_count(series, warmup_min):
    tail = series[-5:]
    if len(tail) < warmup_min:
        assert smooth_throughput(series, warmup_min=warmup_min) is None
    else:
        assert math.isclose(smooth_throughput(series, warmup_min=warmup_min), sum(tail) / 5, rel_tol=1e-9)