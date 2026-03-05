import math
from hypothesis import given, assume, strategies as st

def plan_desk_slot(existing, interval):
    start, end = interval
    if start >= end:
        raise ValueError("invalid interval")

    for s, e in existing:
        if not (end <= s or start >= e):
            return False, existing

    updated = existing + [interval]
    updated.sort()
    return True, updated

@given(st.lists(st.tuples(st.integers(), st.integers()).map(lambda x: (min(x), max(x))), min_size=1), st.tuples(st.integers(), st.integers())
def test_valid_interval(existing, interval):
    assume(interval[0] < interval[1])
    result, _ = plan_desk_slot(existing, interval)
    assert result

@given(st.lists(st.tuples(st.integers(), st.integers()).map(lambda x: (min(x), max(x))), min_size=1), st.tuples(st.integers(), st.integers())
def test_invalid_interval_handling(existing, interval):
    assume(interval[0] >= interval[1])
    try:
        plan_desk_slot(existing, interval)
    except ValueError:
        pass
    else:
        assert False

@given(st.lists(st.tuples(st.integers(), st.integers()).map(lambda x: (min(x), max(x))), min_size=1), st.tuples(st.integers(), st.integers())
def test_no_overlap_check(existing, interval):
    assume(all(interval[1] <= s or interval[0] >= e for s, e in existing))
    result, _ = plan_desk_slot(existing, interval)
    assert result

@given(st.lists(st.tuples(st.integers(), st.integers()).map(lambda x: (min(x), max(x))), min_size=1), st.tuples(st.integers(), st.integers())
def test_overlap_detection(existing, interval):
    assume(any(not (interval[1] <= s or interval[0] >= e) for s, e in existing))
    result, _ = plan_desk_slot(existing, interval)
    assert not result