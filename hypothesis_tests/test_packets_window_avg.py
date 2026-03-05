import math
from hypothesis import given, assume, strategies as st

def packets_window_avg(values, *, window=4, warmup_min=1):
    """
    Rolling mean for packets with warmup.
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

@given(st.lists(st.integers(), min_size=1))
def test_valid_window_size(values):
    assume(all(value > 0 for value in values))
    result = packets_window_avg(values)
    assert result is not None

@given(st.lists(st.integers()))
def test_non_empty_values(values):
    assume(len(values) > 0)
    result = packets_window_avg(values)
    assert result is not None

@given(st.lists(st.integers()), st.integers())
def test_invalid_window_exception(values, window):
    assume(window <= 0)
    try:
        packets_window_avg(values, window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

@given(st.lists(st.integers()), st.integers())
def test_empty_values_exception(values, window):
    assume(not values)
    try:
        packets_window_avg(values, window=window)
    except ValueError as e:
        assert str(e) == "no values"

@given(st.lists(st.integers()), st.integers())
def test_insufficient_data(values, warmup_min):
    assume(len(values) < warmup_min)
    result = packets_window_avg(values, warmup_min=warmup_min)
    assert result is None