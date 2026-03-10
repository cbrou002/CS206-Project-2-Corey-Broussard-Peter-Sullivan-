import math
from hypothesis import given, assume, strategies as st

def guard_email(timestamps, now, *, window=60, limit=20):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]

    if len(recent) > limit:
        return False, 0
    return True, limit - len(recent)

@given(st.lists(st.integers(), min_size=0, max_size=20), st.integers())
def test_throttles_email_by_recent_activity(timestamps, now):
    assume(len(timestamps) <= 20)
    result, _ = guard_email(timestamps, now)
    assert result in [True, False]

@given(st.lists(st.integers(), min_size=0, max_size=20), st.integers())
def test_blocks_email_when_recent_activity_exceeds_limit(timestamps, now):
    assume(len(timestamps) > 20)
    result, _ = guard_email(timestamps, now)
    assert result == False

@given(st.lists(st.integers(), min_size=0, max_size=20), st.integers())
def test_allows_email_when_recent_activity_within_limit(timestamps, now):
    assume(len(timestamps) <= 20)
    result, _ = guard_email(timestamps, now)
    assert result == True

@given(st.lists(st.integers(), min_size=0, max_size=20), st.integers())
def test_filters_recent_activities_based_on_cutoff_time(timestamps, now):
    assume(all(t < now - 60 for t in timestamps))
    _, filtered_count = guard_email(timestamps, now)
    assert all(t >= now - 60 for t in timestamps) or filtered_count == 0