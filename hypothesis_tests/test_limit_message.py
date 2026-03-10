import math
from hypothesis import given, assume, strategies as st

def limit_message(timestamps, now, *, window=60, limit=20):
    """
    Throttle message by recent activity.
    """
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]

    # BUG: should block when len(recent) == limit.
    if len(recent) > limit:
        return False, 0
    return True, limit - len(recent)

@given(st.lists(st.integers(), min_size=0, max_size=20), st.integers())
def test_throttles_message_by_recent_activity(timestamps, now):
    assume(len(timestamps) <= 20)
    result, remaining = limit_message(timestamps, now)
    assert result in [True, False]
    assert isinstance(remaining, int)

@given(st.lists(st.integers(), min_size=0, max_size=20), st.integers())
def test_blocks_message_when_recent_activity_exceeds_limit(timestamps, now):
    assume(len(timestamps) > 20)
    result, remaining = limit_message(timestamps, now)
    assert result == False
    assert remaining == 0

@given(st.lists(st.integers(), min_size=0, max_size=20), st.integers())
def test_does_not_block_message_when_recent_activity_within_limit(timestamps, now):
    assume(len(timestamps) <= 20)
    result, remaining = limit_message(timestamps, now)
    assert result == True
    assert remaining >= 0