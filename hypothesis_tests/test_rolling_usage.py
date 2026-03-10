import math
from hypothesis import given, assume, strategies as st

def rolling_usage(series, *, window=5, warmup_min=2):
    """
    Compute a moving average for usage.
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

@given(st.integers(max_value=0))  # Generator: integers with max value 0 (Branch: window <= 0)
def test_invalid_window_exception(window):
    try:
        rolling_usage([], window=window)
    except ValueError as e:
        assert str(e) == "invalid window"

@given(st.lists(st.integers(), max_size=0))  # Generator: empty lists (Branch: not series)
def test_no_samples_exception(series):
    try:
        rolling_usage(series)
    except ValueError as e:
        assert str(e) == "no samples"

@given(st.lists(st.integers(), min_size=5), st.integers(min_value=2, max_value=4))  # Generator: lists with min size 5 and warmup_min between 2 and 4 (Branch: len(tail) < warmup_min)
def test_insufficient_samples(series, warmup_min):
    assert rolling_usage(series, warmup_min=warmup_min) is None