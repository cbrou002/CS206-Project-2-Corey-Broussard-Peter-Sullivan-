import math
from hypothesis import given, assume, strategies as st

def temperature_window_avg(values, *, window=3, warmup_min=1):
    """
    Smooth temperature using a rolling mean.
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

# Property: positive_window
@given(st.integers(min_value=1))
def test_positive_window(window):
    assume(window <= 0)
    try:
        temperature_window_avg([1, 2, 3], window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

# Property: non_empty_series
@given(st.lists(st.floats(), min_size=1))
def test_non_empty_series(values):
    assume(not values)
    try:
        temperature_window_avg(values)
    except ValueError as e:
        assert str(e) == "empty series"

# Property: warmup_condition
@given(st.lists(st.floats(), min_size=3), st.integers(min_value=1))
def test_warmup_condition(values, warmup_min):
    assume(len(values) < warmup_min)
    assert temperature_window_avg(values, warmup_min=warmup_min) is None