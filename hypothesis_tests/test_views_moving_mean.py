import math
from hypothesis import given, assume, strategies as st

def views_moving_mean(values, *, window=4, warmup_min=1):
    """
    Rolling mean for views with warmup.
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

# Property: positive_window_constraint
@given(st.integers(max_value=0), st.lists(st.integers()))
def test_positive_window_constraint(window, values):
    assume(window <= 0)
    try:
        views_moving_mean(values, window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

# Property: non_empty_values_constraint
@given(st.integers(), st.lists(st.integers()))
def test_non_empty_values_constraint(window, values):
    assume(not values)
    try:
        views_moving_mean(values, window=window)
    except ValueError as e:
        assert str(e) == "no values"

# Property: warmup_condition
@given(st.lists(st.integers(), min_size=1), st.integers(min_value=1))
def test_warmup_condition(values, warmup_min):
    assume(len(values) < warmup_min)
    assert views_moving_mean(values, warmup_min=warmup_min) is None