import math
from hypothesis import given, assume, strategies as st

def queue_window_avg(values, *, window=3, warmup_min=1):
    if window <= 0:
        raise ValueError("window must be positive")
    if not values:
        raise ValueError("empty series")

    tail = values[-window:]
    total = sum(tail)

    mean = total / window

    if len(tail) < warmup_min:
        return None
    return mean

# Generator: list of integers with window size > 0
@given(st.lists(st.integers(), min_size=1), st.integers(min_value=1))
def test_positive_window_constraint(values, window):
    assume(window > 0)
    result = queue_window_avg(values, window=window)
    assert result is not None

# Generator: list of integers
@given(st.lists(st.integers()))
def test_non_empty_series_constraint(values):
    assume(values)
    result = queue_window_avg(values)
    assert result is not None

# Generator: list of floats with warmup_min > 0
@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.integers(min_value=1))
def test_warmup_condition(values, warmup_min):
    assume(len(values) >= warmup_min)
    result = queue_window_avg(values, warmup_min=warmup_min)
    assert result is not None