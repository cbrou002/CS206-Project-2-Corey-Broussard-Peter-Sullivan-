import math
from hypothesis import given, assume, strategies as st

def reservation_overlap_check(reservations, candidate):
    c_start, c_end = candidate
    if c_start >= c_end:
        raise ValueError("invalid reservation")

    for start, end in reservations:
        if not (c_end <= start or c_start >= end):
            return True
    return False

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1), st.tuples(st.integers(), st.integers()))
def test_valid_input_check(reservations, candidate):
    assume(candidate[0] >= candidate[1])
    assert reservation_overlap_check(reservations, candidate) == False

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1), st.tuples(st.integers(), st.integers()))
def test_overlap_condition(reservations, candidate):
    overlap_found = False
    for start, end in reservations:
        if not (candidate[1] <= start or candidate[0] >= end):
            overlap_found = True
            break
    assert reservation_overlap_check(reservations, candidate) == overlap_found

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1), st.tuples(st.integers(), st.integers()))
def test_early_return_true(reservations, candidate):
    overlap_found = False
    for start, end in reservations:
        if not (candidate[1] <= start or candidate[0] >= end):
            overlap_found = True
            break
    if overlap_found:
        assert reservation_overlap_check(reservations, candidate) == True
    else:
        assert reservation_overlap_check(reservations, candidate) == False