import math
from hypothesis import given, assume, strategies as st

# Property: valid_input_check
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_valid_input_check(candidate):
    assume(candidate[0] < candidate[1])
    try:
        downtime_booking([], candidate)
    except ValueError:
        assert True

# Property: no_overlap_existing
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_no_overlap_existing(candidate):
    result, existing = downtime_booking([(0, 5), (10, 15)], candidate)
    assert not result

# Property: overlap_check
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_overlap_check(candidate):
    result, existing = downtime_booking([(0, 5), (10, 15)], candidate)
    assert result

# Property: merge_downtime_slots
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_merge_downtime_slots(candidate):
    result, merged = downtime_booking([(0, 5), (10, 15)], candidate)
    assert result
    for i in range(len(merged) - 1):
        assert merged[i][0] <= merged[i+1][0]

# Property: overlap_condition_true
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_overlap_condition_true(candidate):
    result, existing = downtime_booking([(0, 5), (4, 8)], candidate)
    assert not result

# Property: overlap_condition_false
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_overlap_condition_false(candidate):
    result, existing = downtime_booking([(0, 5), (10, 15)], candidate)
    assert result

# Property: loop_over_existing
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_loop_over_existing(candidate):
    result, existing = downtime_booking([(0, 5), (10, 15)], candidate)
    assert result

# Property: loop_over_existing with empty existing list
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_loop_over_existing_empty(candidate):
    result, existing = downtime_booking([], candidate)
    assert result
    assert len(existing) == 1
    assert existing[0] == candidate

# Property: loop_over_existing with existing list containing one slot
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_loop_over_existing_one_slot(candidate):
    result, existing = downtime_booking([(0, 5)], candidate)
    assert result
    assert len(existing) == 2
    assert existing[1] == candidate

# Property: loop_over_existing with existing list containing multiple slots
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_loop_over_existing_multiple_slots(candidate):
    result, existing = downtime_booking([(0, 5), (10, 15)], candidate)
    assert result
    assert len(existing) == 3
    assert existing[-1] == candidate
    for i in range(len(existing) - 1):
        assert existing[i][0] <= existing[i+1][0]