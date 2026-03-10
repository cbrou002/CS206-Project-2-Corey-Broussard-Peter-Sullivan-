import math
from hypothesis import given, assume, strategies as st

def plan_upgrade_slot(timeline, window):
    a, b = window
    if a >= b:
        raise ValueError("empty window")

    if any(not (b <= s or a >= e) for s, e in timeline):
        return False, timeline

    result = sorted(timeline + [window])
    return True, result

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1), st.tuples(st.integers(), st.integers()))
def test_valid_input_check(timeline, window):
    assume(window[0] < window[1])
    assert plan_upgrade_slot(timeline, window)[0] == True

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1), st.tuples(st.integers(), st.integers()))
def test_timeline_overlap_check(timeline, window):
    assume(any(not (window[1] <= s or window[0] >= e) for s, e in timeline))
    assert plan_upgrade_slot(timeline, window)[0] == False

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1), st.tuples(st.integers(), st.integers()))
def test_allow_partial_overlap(timeline, window):
    assume(not any(not (window[1] <= s or window[0] >= e) for s, e in timeline))
    assert plan_upgrade_slot(timeline, window)[0] == True