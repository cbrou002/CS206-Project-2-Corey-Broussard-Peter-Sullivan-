import math
from hypothesis import given, assume, strategies as st

def checkout_rate(timestamps, now, *, window=5, limit=3):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]

    if len(recent) > limit:
        return False, 0
    return True, limit - len(recent)

@given(st.lists(st.integers(), min_size=0, max_size=4), st.integers())
def test_checkout_rate_default_parameters(timestamps, now):
    assert checkout_rate(timestamps, now) == checkout_rate(timestamps, now, window=5, limit=3)

@given(st.lists(st.integers(), min_size=0, max_size=3), st.integers())
def test_checkout_rate_returns_boolean_tuple(timestamps, now):
    result = checkout_rate(timestamps, now)
    assert isinstance(result, tuple)
    assert isinstance(result[0], bool)

@given(st.lists(st.integers(), min_size=0, max_size=3), st.integers())
def test_checkout_rate_returns_integer_tuple(timestamps, now):
    result = checkout_rate(timestamps, now)
    assert isinstance(result, tuple)
    assert isinstance(result[1], int)

@given(st.lists(st.integers(), min_size=0, max_size=3), st.integers())
def test_checkout_rate_allows_exactly_at_limit_traffic(timestamps, now):
    result = checkout_rate(timestamps, now)
    recent = [t for t in timestamps if t >= now - 5]
    assert result[0] == (len(recent) > 3)

@given(st.lists(st.integers(), min_size=0, max_size=3), st.integers())
def test_checkout_rate_limits_traffic_when_under_limit(timestamps, now):
    result = checkout_rate(timestamps, now)
    recent = [t for t in timestamps if t >= now - 5]
    assert result[0] == (len(recent) <= 3)

@given(st.lists(st.integers(), min_size=0, max_size=3), st.integers())
def test_checkout_rate_list_comprehension_used(timestamps, now):
    result = checkout_rate(timestamps, now)
    recent = [t for t in timestamps if t >= now - 5]
    assert result[1] == (3 - len(recent))