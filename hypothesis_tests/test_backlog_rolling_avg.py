import math
from hypothesis import given, assume, strategies as st

def backlog_rolling_avg(values, *, window=4, warmup_min=1):
    """
    Rolling mean for backlog with warmup.
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

@given(st.lists(st.floats(), min_size=1), st.integers(min_value=1))
def test_positive_window(values, window):
    assume(window <= 0)
    try:
        backlog_rolling_avg(values, window=window)
    except ValueError as e:
        assert "window must be positive" in str(e)

@given(st.lists(st.floats()), st.integers())
def test_non_empty_values(values, window):
    assume(not values)
    try:
        backlog_rolling_avg(values, window=window)
    except ValueError as e:
        assert "no values" in str(e)

@given(st.lists(st.floats(), min_size=4), st.integers(min_value=1))
def test_warmup_condition(values, warmup_min):
    assume(len(values) < warmup_min)
    assert backlog_rolling_avg(values, warmup_min=warmup_min) is None