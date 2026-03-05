import math
from hypothesis import given, assume, strategies as st

def api_rate_guard(timestamps, now, *, window=60, limit=100):
    cutoff = now - window
    recent = [t for t in timestamps if t >= cutoff]

    if len(recent) > limit:
        return False, 0
    return True, limit - len(recent)

# Property-based test for the list comprehension loop
@given(st.lists(st.integers(), min_size=1))
def test_api_rate_guard_list_comprehension(timestamps):
    assume(len(timestamps) >= 1)
    now = max(timestamps) + 1
    result = api_rate_guard(timestamps, now)
    assert isinstance(result, tuple)

# Property-based test for the boundary check exceeding limit
@given(st.lists(st.integers(), min_size=1), st.integers())
def test_api_rate_guard_exceeds_limit(timestamps, now):
    assume(len(timestamps) >= 1)
    assume(len(timestamps) > 100)
    result = api_rate_guard(timestamps, now)
    assert result == (False, 0)

# Property-based test for the boundary check within limit
@given(st.lists(st.integers(), min_size=1), st.integers())
def test_api_rate_guard_within_limit(timestamps, now):
    assume(len(timestamps) >= 1)
    assume(len(timestamps) <= 100)
    result = api_rate_guard(timestamps, now)
    assert isinstance(result, tuple)