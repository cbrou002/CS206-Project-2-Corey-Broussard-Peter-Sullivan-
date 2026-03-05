import math
from hypothesis import given, assume, strategies as st

def maintenance_booking(timeline, window):
    a, b = window
    if a >= b:
        raise ValueError("empty window")

    if any(not (b <= s or a >= e) for s, e in timeline):
        return False, timeline

    result = sorted(timeline + [window])
    return True, result

@given(st.integers(), st.integers())
def test_valid_window_check(a, b):
    assume(a >= 0 and b >= 0)
    assume(a < b)
    assert a < b

@given(st.lists(st.tuples(st.integers(), st.integers())), st.tuples(st.integers(), st.integers()))
def test_timeline_overlap_check(timeline, window):
    assume(all(s < e for s, e in timeline))
    assume(window[0] < window[1])
    assume(all(not (window[1] <= s or window[0] >= e) for s, e in timeline))
    assert all(not (window[1] <= s or window[0] >= e) for s, e in timeline)

@given(st.integers(), st.integers())
def test_empty_window_exception(a, b):
    assume(a >= b)
    try:
        maintenance_booking([(0, 5), (10, 15)], (a, b))
    except ValueError:
        assert True

@given(st.lists(st.tuples(st.integers(), st.integers())), st.tuples(st.integers(), st.integers()))
def test_valid_window_insertion(timeline, window):
    assume(all(s < e for s, e in timeline))
    assume(window[0] < window[1])
    assume(all(not (window[1] <= s or window[0] >= e) for s, e in timeline))
    assert maintenance_booking(timeline, window)[0] is True