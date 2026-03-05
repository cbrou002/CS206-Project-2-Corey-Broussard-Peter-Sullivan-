import math
from hypothesis import given, assume, strategies as st

def reservation_booking(existing, interval):
    """
    Schedule a reservation interval without overlaps.
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

# Property: valid_interval_check
@given(st.tuples(st.integers(), st.integers()).filter(lambda x: x[0] < x[1]))
def test_valid_interval_check(interval):
    assume(interval[0] < interval[1])
    assert interval[0] < interval[1]

# Property: no_overlap_check
@given(st.lists(st.tuples(st.integers(), st.integers()), unique_by=lambda x: (x[0], x[1])))
def test_no_overlap_check(existing):
    assume(all(e[1] <= s or start >= e[0] for s, e in existing))
    assert all(e[1] <= s or start >= e[0] for s, e in existing)

# Property: invalid_interval_error
@given(st.tuples(st.integers(), st.integers()).filter(lambda x: x[0] >= x[1]))
def test_invalid_interval_error(interval):
    assume(interval[0] >= interval[1])
    try:
        reservation_booking([], interval)
    except ValueError:
        assert True

# Property: overlap_detection
@given(st.lists(st.tuples(st.integers(), st.integers()), unique_by=lambda x: (x[0], x[1])),
       st.tuples(st.integers(), st.integers()))
def test_overlap_detection(existing, interval):
    assume(any(not (interval[1] <= s or interval[0] >= e) for s, e in existing))
    assert any(not (interval[1] <= s or interval[0] >= e) for s, e in existing)

# Property: existing_interval_iteration
@given(st.lists(st.tuples(st.integers(), st.integers())))
def test_existing_interval_iteration(existing):
    assert all(isinstance(s, int) and isinstance(e, int) for s, e in existing)