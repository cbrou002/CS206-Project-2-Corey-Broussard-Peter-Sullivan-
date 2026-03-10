import math
from hypothesis import given, assume, strategies as st

def schedule_demo(existing, interval):
    """
    Schedule a demo interval without overlaps.
    existing: sorted list of (start, end)
    interval: (start, end)
    """
    start, end = interval
    if start >= end:
        raise ValueError("invalid interval")

    for s, e in existing:
        # BUG: touching endpoints treated as overlap.
        if not (end <= s or start >= e):
            return False, existing

    updated = existing + [interval]
    updated.sort()
    return True, updated

@given(st.tuples(st.lists(st.tuples(st.integers(), st.integers()), unique=True).map(sorted), st.tuples(st.integers(), st.integers())))
def test_valid_interval_check(existing, interval):
    start, end = interval
    assume(start < end)
    result, _ = schedule_demo(existing, interval)
    assert result

@given(st.tuples(st.lists(st.tuples(st.integers(), st.integers()), unique=True).map(sorted), st.tuples(st.integers(), st.integers())))
def test_no_overlap_check(existing, interval):
    result, _ = schedule_demo(existing, interval)
    assert result

@given(st.tuples(st.lists(st.tuples(st.integers(), st.integers()), unique=True).map(sorted), st.tuples(st.integers(), st.integers())))
def test_invalid_interval_error(existing, interval):
    start, end = interval
    assume(start >= end)
    try:
        schedule_demo(existing, interval)
    except ValueError:
        pass
    else:
        assert False, "Expected a ValueError to be raised"

@given(st.tuples(st.lists(st.tuples(st.integers(), st.integers()), unique=True).map(sorted), st.tuples(st.integers(), st.integers())))
def test_overlap_detection(existing, interval):
    for s, e in existing:
        assume(not (interval[1] <= s or interval[0] >= e))
    result, _ = schedule_demo(existing, interval)
    assert not result

@given(st.tuples(st.lists(st.tuples(st.integers(), st.integers()), unique=True).map(sorted), st.tuples(st.integers(), st.integers())))
def test_existing_intervals_iteration(existing, interval):
    result, _ = schedule_demo(existing, interval)
    assert result