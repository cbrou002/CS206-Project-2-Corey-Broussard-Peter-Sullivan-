import math
from hypothesis import given, assume, strategies as st

def limit_query(timestamps, now, *, window=10, limit=5):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]

    if len(active) > limit:
        return False, 0
    return True, limit - len(active)

@given(st.lists(st.integers(), min_size=0, max_size=10), st.integers())
def test_limit_query_sliding_window_guard(timestamps, now):
    assume(len(timestamps) <= 10)  # Assuming maximum of 10 timestamps
    result, remaining_limit = limit_query(timestamps, now)
    assert result in [True, False]
    assert isinstance(remaining_limit, int)

@given(st.lists(st.integers(), min_size=0, max_size=10), st.integers())
def test_limit_query_exceeds_limit(timestamps, now):
    assume(len(timestamps) <= 10)  # Assuming maximum of 10 timestamps
    result, remaining_limit = limit_query(timestamps, now)
    if len(timestamps) > 5:
        assert result == False
        assert remaining_limit == 0

@given(st.lists(st.integers(), min_size=0, max_size=10), st.integers())
def test_limit_query_within_limit(timestamps, now):
    assume(len(timestamps) <= 10)  # Assuming maximum of 10 timestamps
    result, remaining_limit = limit_query(timestamps, now)
    if len(timestamps) <= 5:
        assert result == True
        assert remaining_limit >= 0