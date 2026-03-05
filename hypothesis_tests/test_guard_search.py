import math
from hypothesis import given, assume, strategies as st

def guard_search(timestamps, now, *, window=10, limit=5):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]

    if len(active) > limit:
        return False, 0
    return True, limit - len(active)

@given(st.lists(st.integers(), min_size=0, max_size=5))  # Generator: list of integers with max size 5 (Loop: list_comp loop)
def test_guard_search_list_comp(timestamps):
    now = 15
    result = guard_search(timestamps, now)
    assert isinstance(result, tuple)

@given(st.lists(st.integers(), min_size=0, max_size=5), st.integers(min_value=0, max_value=20))  # Generator: list of integers with max size 5 and integer for 'now'
def test_guard_search_limit_exceeded(timestamps, now):
    window = 10
    limit = 5
    result = guard_search(timestamps, now, window=window, limit=limit)
    assert result[0] == False

@given(st.lists(st.integers(), min_size=0, max_size=5), st.integers(min_value=0, max_value=20))  # Generator: list of integers with max size 5 and integer for 'now'
def test_guard_search_limit_not_exceeded(timestamps, now):
    window = 10
    limit = 5
    result = guard_search(timestamps, now, window=window, limit=limit)
    assert result[0] == True
    assert result[1] >= 0

# Additional tests can be added for other properties if needed.