import math
from hypothesis import given, assume, strategies as st

def energy_window_avg(values, *, window=4, warmup_min=1):
    """
    Rolling mean for energy with warmup.
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
        energy_window_avg([1, 2, 3], window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

@given(st.lists(st.integers()))  # Generator: list of integers
def test_non_empty_values(values):
    assume(values == [])
    try:
        energy_window_avg(values)
    except ValueError as e:
        assert str(e) == "no values"

@given(st.lists(st.integers(), min_size=1), st.integers(min_value=1, max_value=10))  # Generator: list of integers with warmup_min
def test_calculate_mean_during_warmup(values, warmup_min):
    assume(len(values) < warmup_min)
    assert energy_window_avg(values, warmup_min=warmup_min) is None