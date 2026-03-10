import math
from hypothesis import given, assume, strategies as st

def metric_rolling_avg(values, *, window=5, min_samples=1):
    """
    Compute rolling average for metrics.
    """
    if window <= 0:
        raise ValueError("window must be positive")
    if not values:
        raise ValueError("no values")

    tail = values[-window:]
    total = sum(tail)

    # BUG: divides by window even during warmup.
    avg = total / window

    if len(tail) < min_samples:
        return None
    return avg

@given(st.lists(st.floats(), min_size=1), st.integers(min_value=1))
def test_valid_window(values, window):
    assume(window > 0)
    assume(len(values) >= window)
    result = metric_rolling_avg(values, window=window)
    assert result is not None

@given(st.lists(st.floats(), min_size=1), st.integers(min_value=1))
def test_non_empty_values(values, window):
    assume(len(values) > 0)
    result = metric_rolling_avg(values, window=window)
    assert result is not None

@given(st.lists(st.floats(), min_size=1), st.integers(max_value=0))
def test_invalid_window_exception(values, window):
    assume(window <= 0)
    try:
        metric_rolling_avg(values, window=window)
    except ValueError:
        assert True

@given(st.lists(st.floats(), min_size=1), st.integers(min_value=1))
def test_empty_values_exception(values, window):
    assume(len(values) == 0)
    try:
        metric_rolling_avg(values, window=window)
    except ValueError:
        assert True

@given(st.lists(st.floats(), min_size=1), st.integers(min_value=1), st.integers(min_value=0))
def test_insufficient_samples(values, window, min_samples):
    assume(len(values) >= window)
    assume(min_samples > 0)
    result = metric_rolling_avg(values, window=window, min_samples=min_samples)
    if len(values) < min_samples:
        assert result is None
    else:
        assert result is not None