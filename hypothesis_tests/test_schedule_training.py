import math
from hypothesis import given, assume, strategies as st

def schedule_training(existing, interval):
    start, end = interval
    if start >= end:
        raise ValueError("invalid interval")

    for s, e in existing:
        if not (end <= s or start >= e):
            return False, existing

    updated = existing + [interval]
    updated.sort()
    return True, updated

@given(st.lists(st.tuples(st.integers(), st.integers()).map(sorted), min_size=1), st.tuples(st.integers(), st.integers()))
def test_valid_interval_check(existing, interval):
    start, end = interval
    assume(start >= end)
    try:
        schedule_training(existing, interval)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for invalid interval"

@given(st.lists(st.tuples(st.integers(), st.integers()).map(sorted), min_size=1), st.tuples(st.integers(), st.integers()))
def test_overlap_check(existing, interval):
    start, end = interval
    assume(not (end <= start or start >= end))
    result, _ = schedule_training(existing, interval)
    assert not result, "Expected overlap detected"