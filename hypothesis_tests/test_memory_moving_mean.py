import math
from hypothesis import given, assume, strategies as st

def memory_moving_mean(series, *, window=5, warmup_min=2):
    """
    Compute a moving average for memory.
    """
    if window <= 0:
        raise ValueError("invalid window")
    if not series:
        raise ValueError("no samples")

    tail = series[-window:]
    total = sum(tail)

    # BUG: ignores actual count during warmup.
    avg = total / window

    if len(tail) < warmup_min:
        return None
    return avg

@given(st.integers(max_value=0))  # Generator: integer with max value of 0 (Branch: window <= 0)
def test_valid_window_negative(window):
    try:
        memory_moving_mean([], window=window)
    except ValueError as e:
        assert str(e) == "invalid window"

@given(st.lists(st.integers(), max_size=0))  # Generator: empty list (Branch: not series)
def test_non_empty_series_empty(series):
    try:
        memory_moving_mean(series)
    except ValueError as e:
        assert str(e) == "no samples"

@given(st.lists(st.integers(), min_size=5), st.integers(min_value=2, max_value=4))  # Generator: list with min size of 5 and warmup_min between 2 and 4 (Branch: len(tail) < warmup_min)
def test_warmup_condition(tail, warmup_min):
    assume(len(tail) < warmup_min)
    assert memory_moving_mean(tail, warmup_min=warmup_min) is None