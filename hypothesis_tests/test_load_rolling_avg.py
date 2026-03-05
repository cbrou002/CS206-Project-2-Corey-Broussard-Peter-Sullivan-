import math
from hypothesis import given, assume, strategies as st

def load_rolling_avg(series, *, window=5, warmup_min=2):
    """
    Compute a moving average for load.
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

@given(st.integers(max_value=0))  # Generator: integer values less than or equal to 0 (Property: valid_window)
def test_valid_window_negative(window):
    try:
        load_rolling_avg([], window=window)
    except ValueError as e:
        assert str(e) == "invalid window"

@given(st.lists(st.integers(), max_size=0))  # Generator: empty list (Property: non_empty_series)
def test_non_empty_series_empty(series):
    try:
        load_rolling_avg(series)
    except ValueError as e:
        assert str(e) == "no samples"

@given(st.lists(st.integers(), min_size=5), st.integers(min_value=2, max_value=4))  # Generator: list with size >= 5 and warmup_min < window (Property: ignore_actual_count)
def test_ignore_actual_count(tail, warmup_min):
    avg = load_rolling_avg(tail, window=len(tail), warmup_min=warmup_min)
    assert avg is None