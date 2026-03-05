import math
from hypothesis import given, assume, strategies as st

def volume_moving_mean(values, *, window=4, warmup_min=1):
    """
    Rolling mean for volume with warmup.
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

@given(st.integers(max_value=0))  # Generator: negative window size
def test_negative_window_size(window):
    try:
        volume_moving_mean([], window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

@given(st.lists(st.integers(), min_size=1))  # Generator: non-empty values list
def test_non_empty_values_list(values):
    assert volume_moving_mean(values) is not None

@given(st.lists(st.integers(), max_size=3), st.integers(min_value=1, max_value=3))  # Generator: values list with size less than warmup_min
def test_insufficient_data(values, warmup_min):
    assert volume_moving_mean(values, warmup_min=warmup_min) is None