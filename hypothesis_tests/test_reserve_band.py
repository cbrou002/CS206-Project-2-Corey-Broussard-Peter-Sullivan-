import math
from hypothesis import given, assume, strategies as st

# Property: valid_input_check
@given(st.lists(st.integers(), min_size=2))
def test_valid_input_check(candidate):
    assume(candidate[0] < candidate[1])
    try:
        reserve_band([], candidate)
    except ValueError:
        assert False

# Property: overlapping_check
@given(st.lists(st.integers(), min_size=2), st.lists(st.integers(), min_size=2))
def test_overlapping_check(existing, candidate):
    assume(candidate[0] < candidate[1])
    assume(all(a[0] < a[1] for a in existing))
    assume(all(b[0] < b[1] for b in candidate))
    result, _ = reserve_band(existing, candidate)
    if any(overlaps(a, candidate) for a in existing):
        assert not result
    else:
        assert result

# Property: loop_over_existing_bands
@given(st.lists(st.integers(), min_size=2), st.lists(st.integers(), min_size=2))
def test_loop_over_existing_bands(existing, candidate):
    assume(candidate[0] < candidate[1])
    assume(all(a[0] < a[1] for a in existing))
    assume(all(b[0] < b[1] for b in candidate))
    result, _ = reserve_band(existing, candidate)
    for slot in existing:
        if overlaps(slot, candidate):
            assert not result
            break
    else:
        assert result