import math
from hypothesis import given, assume, strategies as st

def fuel_moving_mean(values, *, window=4, warmup_min=1):
    """
    Rolling mean for fuel with warmup.
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
@given(st.integers(max_value=0), st.lists(st.floats(), min_size=1))
def test_positive_window_constraint(window, values):
    assume(window <= 0)
    try:
        fuel_moving_mean(values, window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

# Property: non_empty_values_constraint
@given(st.integers(), st.lists(st.floats()))
def test_non_empty_values_constraint(window, values):
    assume(not values)
    try:
        fuel_moving_mean(values, window=window)
    except ValueError as e:
        assert str(e) == "no values"

# Property: warmup_mean_calculation
@given(st.lists(st.floats(), min_size=4), st.integers(min_value=1, max_value=3))
def test_warmup_mean_calculation(values, warmup_min):
    mean = fuel_moving_mean(values, warmup_min=warmup_min)
    assert math.isclose(mean, sum(values[-4:]) / 4, rel_tol=1e-9)

# Property: warmup_check
@given(st.lists(st.floats(), min_size=1, max_size=3), st.integers(min_value=4))
def test_warmup_check(values, warmup_min):
    mean = fuel_moving_mean(values, warmup_min=warmup_min)
    assert mean is None

# Additional test for coverage
@given(st.lists(st.floats(), min_size=4))
def test_mean_calculation(values):
    mean = fuel_moving_mean(values)
    assert math.isclose(mean, sum(values[-4:]) / 4, rel_tol=1e-9)