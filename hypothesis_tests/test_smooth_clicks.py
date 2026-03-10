import math
from hypothesis import given, assume, strategies as st

def smooth_clicks(values, *, window=3, warmup_min=1):
    """
    Smooth clicks using a rolling mean.
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

# Property: The window parameter must be positive.
@given(st.integers(max_value=0))
def test_positive_window(window):
    assume(window <= 0)
    try:
        smooth_clicks([1, 2, 3], window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

# Property: The values parameter must not be empty.
@given(st.lists(st.integers(), min_size=1))
def test_non_empty_values(values):
    try:
        smooth_clicks(values)
    except ValueError as e:
        assert str(e) == "empty series"

# Property: Checks if the window parameter is less than or equal to 0.
@given(st.lists(st.integers()), st.integers(max_value=0))
def test_window_positive_check(values, window):
    assume(window <= 0)
    try:
        smooth_clicks(values, window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

# Property: Checks if the values parameter is empty.
@given(st.lists(st.integers()))
def test_non_empty_series_check(values):
    assume(not values)
    try:
        smooth_clicks(values)
    except ValueError as e:
        assert str(e) == "empty series"

# Property: Checks if the length of tail is less than warmup_min.
@given(st.lists(st.integers()), st.integers(min_value=1))
def test_warmup_min_check(values, warmup_min):
    try:
        smooth_clicks(values, warmup_min=warmup_min)
    except ValueError as e:
        assert str(e) == "empty series"