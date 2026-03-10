import math
from hypothesis import given, assume, strategies as st

def login_throttle(timestamps, now, *, window=60, limit=20):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]

    if len(recent) > limit:
        return False, 0
    return True, limit - len(recent)

@given(st.lists(st.integers(), min_size=1))
def test_login_throttle_list_comprehension(timestamps):
    assume(len(timestamps) > 0)
    now = max(timestamps) + 1
    result = login_throttle(timestamps, now)
    assert isinstance(result, tuple)

@given(st.lists(st.integers(), min_size=1))
def test_login_throttle_blocks_when_recent_exceeds_limit(timestamps):
    assume(len(timestamps) > 0)
    now = max(timestamps) + 1
    result = login_throttle(timestamps, now, limit=5)
    assert result[0] == False
    assert result[1] == 0

@given(st.lists(st.integers(), min_size=1))
def test_login_throttle_does_not_block_when_recent_within_limit(timestamps):
    assume(len(timestamps) > 0)
    now = max(timestamps) + 1
    result = login_throttle(timestamps, now, limit=25)
    assert result[0] == True
    assert result[1] == 25 - len([t for t in timestamps if t >= now - 60])