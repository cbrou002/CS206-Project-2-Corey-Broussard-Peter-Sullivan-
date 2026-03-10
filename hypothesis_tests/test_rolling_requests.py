import math
from hypothesis import given, assume, strategies as st

def rolling_requests(series, *, window=5, warmup_min=2):
    """
    Compute a moving average for requests.
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
        rolling_requests([1, 2, 3], window=window)
    except ValueError as e:
        assert str(e) == "invalid window"

@given(st.lists(st.integers(), min_size=1))  # Generator: list of integers with minimum size of 1 (Branch: not series)
def test_non_empty_series(series):
    try:
        rolling_requests(series)
    except ValueError as e:
        assert str(e) == "no samples"

@given(st.lists(st.integers(), min_size=5), st.integers(min_value=0, max_value=4))  # Generator: list of integers with minimum size of 5 and window value less than 5 (Branch: len(tail) < warmup_min)
def test_warmup_condition(series, window):
    assume(len(series) >= window)
    try:
        assert rolling_requests(series, window=window, warmup_min=5) is None
    except ValueError as e:
        assert False, f"Unexpected ValueError: {e}"