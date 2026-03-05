import math
from hypothesis import given, assume, strategies as st

def rolling_retries(values, *, window=3, warmup_min=1):
    """
    Smooth retries using a rolling mean.
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

@given(st.integers(max_value=0))  # Generator: integers with max value of 0 (Branch: window <= 0)
def test_positive_window(window):
    try:
        rolling_retries([1, 2, 3], window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

@given(st.lists(st.integers(), max_size=0))  # Generator: empty list (Branch: not values)
def test_non_empty_series(values):
    try:
        rolling_retries(values)
    except ValueError as e:
        assert str(e) == "empty series"

@given(st.lists(st.integers(), min_size=4), st.integers(min_value=1, max_value=3))  # Generator: list with min size of 4 and warmup_min between 1 and 3 (Branch: len(tail) < warmup_min)
def test_insufficient_data(values, warmup_min):
    assert rolling_retries(values, warmup_min=warmup_min) is None