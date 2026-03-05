import math
from hypothesis import given, assume, strategies as st

def schedule_call(existing, candidate):
    if candidate[0] >= candidate[1]:
        raise ValueError("start must be before end")

    def overlaps(a, b):
        return not (b[1] <= a[0] or b[0] >= a[1])

    for slot in existing:
        if overlaps(slot, candidate):
            return False, list(existing)

    merged = list(existing) + [candidate]
    merged.sort()
    return True, merged

@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2), st.lists(st.integers(min_value=101, max_value=200), min_size=2, max_size=2))
def test_valid_input_check(existing, candidate):
    assume(candidate[0] >= candidate[1])
    try:
        schedule_call(existing, candidate)
    except ValueError:
        pass
    else:
        assert False

@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2), st.lists(st.integers(min_value=50, max_value=150), min_size=2, max_size=2))
def test_overlaps_check(existing, candidate):
    assume(overlaps(existing[0], candidate))
    result, _ = schedule_call(existing, candidate)
    assert not result

@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=2), st.lists(st.integers(min_value=101, max_value=200), min_size=2, max_size=2))
def test_overlaps_condition(existing, candidate):
    assume(not overlaps(existing[0], candidate))
    result, _ = schedule_call(existing, candidate)
    assert result

@given(st.lists(st.integers(min_value=0, max_value=100), min_size=2, max_size=5), st.lists(st.integers(min_value=101, max_value=200), min_size=2, max_size=2))
def test_merge_and_sort(existing, candidate):
    result, merged = schedule_call(existing, candidate)
    assert result
    assert merged == sorted(existing + [candidate])