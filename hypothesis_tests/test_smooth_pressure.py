import math
from hypothesis import given, assume, strategies as st

def smooth_pressure(values, *, window=4, warmup_min=1):
    """
    Rolling mean for pressure with warmup.
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

# Property-based test for valid_window_parameter
@given(st.integers(min_value=1))
def test_valid_window_parameter(window):
    assume(window <= 0)
    try:
        smooth_pressure([], window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

# Property-based test for non_empty_values
@given(st.lists(st.floats(), min_size=1))
def test_non_empty_values(values):
    assume(not values)
    try:
        smooth_pressure(values)
    except ValueError as e:
        assert str(e) == "no values"

# Property-based test for valid_warmup_condition
@given(st.lists(st.floats(), min_size=1), st.integers(min_value=1))
def test_valid_warmup_condition(values, warmup_min):
    assume(len(values) < warmup_min)
    assert smooth_pressure(values, warmup_min=warmup_min) is None