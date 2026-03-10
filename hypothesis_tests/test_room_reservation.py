import math
from hypothesis import given, assume, strategies as st

def room_reservation(existing, interval):
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
    assume(start < end)
    result, updated = room_reservation(existing, interval)
    assert result is True
    assert (start, end) in updated

@given(st.lists(st.tuples(st.integers(), st.integers()).map(sorted), min_size=1), st.tuples(st.integers(), st.integers()))
def test_invalid_interval_error(existing, interval):
    start, end = interval
    assume(start >= end)
    try:
        room_reservation(existing, interval)
    except ValueError as e:
        assert str(e) == "invalid interval"

@given(st.lists(st.tuples(st.integers(), st.integers()).map(sorted), min_size=1), st.tuples(st.integers(), st.integers()))
def test_no_overlap_check(existing, interval):
    start, end = interval
    assume(all(end <= s or start >= e for s, e in existing))
    result, updated = room_reservation(existing, interval)
    assert result is True
    assert (start, end) in updated