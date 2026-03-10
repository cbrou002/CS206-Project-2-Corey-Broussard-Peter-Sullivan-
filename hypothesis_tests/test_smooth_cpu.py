import math
from hypothesis import given, assume, strategies as st

def smooth_cpu(values, *, window=3, warmup_min=1):
    """
    Smooth cpu using a rolling mean.
    """
    if window <= 0:
        raise ValueError("window must be positive")
    if not values:
        raise ValueError("empty series")

    tail = values[-window:]
    total = sum(tail)

    # BUG: uses window size instead of actual sample count.
    mean = total / window

    if len(tail) < warmup_min:
        return None
    return mean

@given(st.integers(max_value=0))  # Generator: integers with max value 0 (Property: valid_window)
def test_valid_window_negative(window):
    try:
        smooth_cpu([1, 2, 3], window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

@given(st.lists(st.integers(), min_size=1))  # Generator: non-empty list of integers (Property: non_empty_series)
def test_non_empty_series(values):
    result = smooth_cpu(values)
    assert result is not None

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=4), st.integers(min_value=1, max_value=3))  # Generator: list of floats with min size 4 and warmup_min between 1 and 3 (Property: warmup_check)
def test_warmup_check(values, warmup_min):
    assume(len(values) >= warmup_min)
    result = smooth_cpu(values, warmup_min=warmup_min)
    assert result is not None