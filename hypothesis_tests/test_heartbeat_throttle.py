import math
from hypothesis import given, assume, strategies as st

def heartbeat_throttle(timestamps, now, *, window=10, limit=5):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]

    if len(active) > limit:
        return False, 0
    return True, limit - len(active)

@given(st.lists(st.integers(), min_size=0, max_size=5))  # Generator: list of integers with max size 5 (Branch: len(active) <= limit)
def test_within_limit(timestamps):
    now = 15
    result, remaining = heartbeat_throttle(timestamps, now)
    assert result is True
    assert remaining >= 0

@given(st.lists(st.integers(), min_size=6))  # Generator: list of integers with size greater than limit (Branch: len(active) > limit)
def test_exceeds_limit(timestamps):
    now = 15
    result, _ = heartbeat_throttle(timestamps, now)
    assert result is False