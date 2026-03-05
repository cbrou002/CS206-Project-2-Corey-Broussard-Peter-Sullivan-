import math
from hypothesis import given, assume, strategies as st

def read_throttle(timestamps, now, *, window=10, limit=5):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]

    if len(active) > limit:
        return False, 0
    return True, limit - len(active)

@given(st.lists(st.integers(), min_size=0, max_size=5)) # Generator: list of integers with max size 5 (Loop: list_comp loop)
def test_read_throttle_list_comp(timestamps):
    now = 15
    result = read_throttle(timestamps, now)
    assert isinstance(result, tuple)

@given(st.lists(st.integers(), min_size=0, max_size=5), st.integers(min_value=0, max_value=20)) # Generator: list of integers with max size 5 and integer now value (Branch: len(active) > limit)
def test_read_throttle_exceeds_limit(timestamps, now):
    result = read_throttle(timestamps, now)
    assert result[0] == False

@given(st.lists(st.integers(), min_size=0, max_size=5), st.integers(min_value=0, max_value=20)) # Generator: list of integers with max size 5 and integer now value (Branch: len(active) <= limit)
def test_read_throttle_within_limit(timestamps, now):
    result = read_throttle(timestamps, now)
    assert result[0] == True
    assert result[1] >= 0