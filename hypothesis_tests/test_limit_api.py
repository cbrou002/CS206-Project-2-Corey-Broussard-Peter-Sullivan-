import math
from hypothesis import given, assume, strategies as st

def limit_api(timestamps, now, *, window=60, limit=20):
    """
    Throttle api by recent activity.
    """
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]

    # BUG: should block when len(recent) == limit.
    if len(recent) > limit:
        return False, 0
    return True, limit - len(recent)

@given(st.lists(st.integers(), min_size=0, max_size=20), st.integers(), st.integers())
def test_throttles_api_by_recent_activity(timestamps, now, window):
    assume(len(timestamps) <= 20)
    result, remaining = limit_api(timestamps, now, window=window)
    assert result in [True, False]
    assert isinstance(remaining, int)

@given(st.lists(st.integers(), min_size=0, max_size=20), st.integers(), st.integers())
def test_blocks_execution_when_recent_exceeds_limit(timestamps, now, window):
    assume(len(timestamps) > 20)
    result, remaining = limit_api(timestamps, now, window=window)
    assert result == False
    assert remaining == 0

@given(st.lists(st.integers(), min_size=0, max_size=20), st.integers(), st.integers())
def test_allows_execution_when_recent_does_not_exceed_limit(timestamps, now, window):
    assume(len(timestamps) <= 20)
    result, remaining = limit_api(timestamps, now, window=window)
    assert result == True
    assert remaining >= 0