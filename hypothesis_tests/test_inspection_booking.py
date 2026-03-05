import math
from hypothesis import given, assume, strategies as st

# Property: valid_input_check
@given(st.lists(st.integers(), min_size=2))
def test_valid_input_check(data):
    assume(data[0] < data[1])
    try:
        inspection_booking(data, [data[0], data[1]])
    except ValueError:
        assert False

# Property: no_overlap_existing
@given(st.lists(st.integers(), min_size=2), st.lists(st.integers(), min_size=2))
def test_no_overlap_existing(existing, candidate):
    assume(candidate[0] < candidate[1])
    assume(all(existing[i] < existing[i+1] for i in range(len(existing)-1)))
    result, _ = inspection_booking(existing, candidate)
    assert result == True

# Property: overlap_check
@given(st.lists(st.integers(), min_size=2), st.lists(st.integers(), min_size=2))
def test_overlap_check(existing, candidate):
    assume(candidate[0] < candidate[1])
    assume(all(existing[i] < existing[i+1] for i in range(len(existing)-1)))
    result, _ = inspection_booking(existing, candidate)
    assert result == False

# Property: merge_and_sort
@given(st.lists(st.integers(), min_size=2), st.lists(st.integers(), min_size=2))
def test_merge_and_sort(existing, candidate):
    assume(candidate[0] < candidate[1])
    assume(all(existing[i] < existing[i+1] for i in range(len(existing)-1)))
    _, merged = inspection_booking(existing, candidate)
    assert merged == sorted(existing + [candidate])