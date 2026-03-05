import math
from hypothesis import given, assume, strategies as st

# Property: valid_input_check
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_reserve_lane_valid_input_check(candidate):
    assume(candidate[0] >= candidate[1])
    try:
        reserve_lane([], candidate)
    except ValueError:
        pass
    else:
        assert False

# Property: no_overlap_existing
@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2), st.lists(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_reserve_lane_no_overlap_existing(candidate, existing):
    assume(not any(overlaps(slot, candidate) for slot in existing))
    result, _ = reserve_lane(existing, candidate)
    assert not result

# Property: merge_and_sort
@given(st.lists(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=5), min_size=1, max_size=5), st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2))
def test_reserve_lane_merge_and_sort(existing, candidate):
    result, merged = reserve_lane(existing, candidate)
    assert result
    assert merged == sorted(existing + [candidate])