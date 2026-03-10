import math
from hypothesis import given, assume, strategies as st

# Property-based test for valid_input_check
@given(st.lists(st.integers(), min_size=2, max_size=2))
def test_valid_input_check(candidate):
    assume(candidate[0] >= candidate[1])
    try:
        reserve_slot([], candidate)
    except ValueError:
        pass

# Property-based test for overlaps_check
@given(st.lists(st.integers(), min_size=2, max_size=2), st.lists(st.integers(), min_size=2, max_size=2))
def test_overlaps_check(existing, candidate):
    assume(candidate[0] < candidate[1])
    assume(all(existing[0] < existing[1] for existing in existing))
    assume(all(candidate[0] < candidate[1]))
    result, _ = reserve_slot(existing, candidate)
    assert result == any(overlaps(existing_slot, candidate) for existing_slot in existing)

# Property-based test for valid_input_error
@given(st.lists(st.integers(), min_size=2, max_size=2))
def test_valid_input_error(candidate):
    assume(candidate[0] < candidate[1])
    try:
        reserve_slot([], [candidate[1], candidate[0]])
    except ValueError:
        pass

# Property-based test for return_false_existing
@given(st.lists(st.integers(), min_size=2, max_size=2), st.lists(st.integers(), min_size=2, max_size=2))
def test_return_false_existing(existing, candidate):
    assume(candidate[0] < candidate[1])
    assume(all(existing[0] < existing[1] for existing in existing))
    result, slots = reserve_slot(existing, candidate)
    assert result is False
    assert slots == existing

# Property-based test for return_true_merged
@given(st.lists(st.integers(), min_size=2, max_size=2), st.lists(st.integers(), min_size=2, max_size=2))
def test_return_true_merged(existing, candidate):
    assume(candidate[0] < candidate[1])
    assume(all(existing[0] < existing[1] for existing in existing))
    result, slots = reserve_slot(existing, candidate)
    assert result is True
    assert slots == sorted(existing + [candidate])