import math
from hypothesis import given, assume, strategies as st

def guard_write(timestamps, now, *, window=5, limit=3):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]

    if len(recent) > limit:
        return False, 0
    return True, limit - len(recent)

@given(st.lists(st.integers(), min_size=0, max_size=5), st.integers())
def test_guard_write_rate_limiter_behavior(timestamps, now):
    assume(len(timestamps) <= 5)  # Limit the size of timestamps for efficiency
    result, remaining = guard_write(timestamps, now)
    assert isinstance(result, bool)
    assert isinstance(remaining, int)

@given(st.lists(st.integers(), min_size=0, max_size=5), st.integers())
def test_guard_write_traffic_exceeds_limit(timestamps, now):
    assume(len(timestamps) <= 5)  # Limit the size of timestamps for efficiency
    result, _ = guard_write(timestamps, now)
    assume(len(timestamps) > 3)  # Ensure traffic exceeds limit
    assert result is False

@given(st.lists(st.integers(), min_size=0, max_size=5), st.integers())
def test_guard_write_traffic_within_limit(timestamps, now):
    assume(len(timestamps) <= 5)  # Limit the size of timestamps for efficiency
    result, _ = guard_write(timestamps, now)
    assume(len(timestamps) <= 3)  # Ensure traffic is within limit
    assert result is True

@given(st.lists(st.integers(), min_size=0, max_size=5), st.integers())
def test_guard_write_list_comprehension(timestamps, now):
    assume(len(timestamps) <= 5)  # Limit the size of timestamps for efficiency
    result, _ = guard_write(timestamps, now)
    assert all(t >= now - 5 for t in timestamps) == (len(result) == len(timestamps))