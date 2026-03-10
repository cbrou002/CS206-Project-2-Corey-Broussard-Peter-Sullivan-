import math
from hypothesis import given, assume, strategies as st

def schedule_pickup(timeline, window):
    a, b = window
    if a >= b:
        raise ValueError("empty window")

    if any(not (b <= s or a >= e) for s, e in timeline):
        return False, timeline

    result = sorted(timeline + [window])
    return True, result

@given(st.integers(), st.integers())
def test_valid_window_check(a, b):
    assume(a >= b)
    try:
        schedule_pickup([], (a, b))
    except ValueError:
        pass

@given(st.lists(st.tuples(st.integers(), st.integers())), st.tuples(st.integers(), st.integers()))
def test_timeline_overlap_check(timeline, window):
    assume(any(not (window[1] <= s or window[0] >= e) for s, e in timeline))
    result = schedule_pickup(timeline, window)
    assert result[0] == False

@given(st.lists(st.tuples(st.integers(), st.integers())), st.tuples(st.integers(), st.integers()))
def test_valid_overlap_condition(timeline, window):
    assume(not any(not (window[1] <= s or window[0] >= e) for s, e in timeline))
    result = schedule_pickup(timeline, window)
    assert result[0] == True