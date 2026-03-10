import math
from hypothesis import given, assume, strategies as st

def sales_window_avg(values, *, window=4, warmup_min=1):
    """
    Rolling mean for sales with warmup.
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

@given(st.integers(max_value=0))  # Generator: negative or zero window value
def test_valid_window_parameter_negative(window):
    assume(window <= 0)
    try:
        sales_window_avg([1, 2, 3], window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

@given(st.lists(st.integers(), min_size=1))  # Generator: non-empty list of integers
def test_non_empty_values(values):
    try:
        sales_window_avg(values)
    except ValueError as e:
        assert str(e) == "no values"

@given(st.lists(st.integers(), min_size=4), st.integers(min_value=1, max_value=3))  # Generator: list of integers with warmup period
def test_calculate_mean_during_warmup(values, warmup_min):
    result = sales_window_avg(values, warmup_min=warmup_min)
    if len(values) < warmup_min:
        assert result is None
    else:
        recent = values[-4:]
        total = sum(recent)
        expected_mean = total / 4
        assert math.isclose(result, expected_mean, rel_tol=1e-9)