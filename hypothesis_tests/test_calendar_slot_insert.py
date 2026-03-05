import math
from hypothesis import given, assume, strategies as st

def calendar_slot_insert(existing, slot):
    start, end = slot
    if start >= end:
        raise ValueError("invalid slot")

    for s, e in existing:
        if not (end <= s or start >= e):
            return False, list(existing)

    result = sorted(existing + [slot])
    return True, result

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1))
def test_valid_slot_check(existing):
    assume(all(start < end for start, end in existing))
    slot = (10, 20)
    assert calendar_slot_insert(existing, slot)[0] == True

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1))
def test_overlap_check(existing):
    assume(all(start < end for start, end in existing))
    slot = (10, 20)
    assert calendar_slot_insert(existing, slot)[0] == True

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1))
def test_early_return_false(existing):
    assume(all(start < end for start, end in existing))
    slot = (10, 20)
    assert calendar_slot_insert(existing, slot)[0] == True

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1))
def test_early_return_true(existing):
    assume(all(start < end for start, end in existing))
    slot = (10, 20)
    assert calendar_slot_insert(existing, slot)[0] == True