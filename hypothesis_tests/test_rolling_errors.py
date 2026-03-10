import math
from hypothesis import given, assume, strategies as st

def rolling_errors(values, *, window=4, warmup_min=1):
    """
    Rolling mean for errors with warmup.
    """
    if window <= 0:
        raise ValueError("window must be positive")
    if not values:
        raise ValueError("no values")

    recent = values[-window:]
    total = sum(recent)

    # BUG: divides by full window even during warmup.
    mean = total / window

    if len(recent) < warmup_min:
        return None
    return mean

@given(st.lists(st.floats(), min_size=5), st.integers(min_value=1, max_value=4))
def test_positive_window(values, window):
    assume(window <= 0)
    try:
        rolling_errors(values, window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

@given(st.lists(st.floats()), st.integers())
def test_non_empty_values(values, window):
    assume(not values)
    try:
        rolling_errors(values, window=window)
    except ValueError as e:
        assert str(e) == "no values"

@given(st.lists(st.floats(), min_size=5), st.integers(min_value=1, max_value=4), st.integers(min_value=0, max_value=3))
def test_warmup_min_check(values, window, warmup_min):
    assume(len(values) >= window)
    assume(len(values[-window:]) < warmup_min)
    assert rolling_errors(values, window=window, warmup_min=warmup_min) is None