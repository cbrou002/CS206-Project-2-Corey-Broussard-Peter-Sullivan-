import math
from hypothesis import given, assume, strategies as st

def plan_appointment_slot(timeline, window):
    a, b = window
    if a >= b:
        raise ValueError("empty window")

    if any(not (b <= s or a >= e) for s, e in timeline):
        return False, timeline

    result = sorted(timeline + [window])
    return True, result

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1), st.tuples(st.integers(), st.integers()))
def test_valid_window_check(timeline, window):
    assume(window[0] < window[1])
    result = plan_appointment_slot(timeline, window)
    assert result[0] == True

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1), st.tuples(st.integers(), st.integers()))
def test_timeline_overlap_check(timeline, window):
    assume(window[0] < window[1])
    result = plan_appointment_slot(timeline, window)
    assert result[0] == True

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1), st.tuples(st.integers(), st.integers()))
def test_empty_window_exception(timeline, window):
    assume(window[0] >= window[1])
    try:
        plan_appointment_slot(timeline, window)
    except ValueError:
        assert True

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1), st.tuples(st.integers(), st.integers()))
def test_overlap_exception_handling(timeline, window):
    assume(any(not (window[1] <= s or window[0] >= e) for s, e in timeline))
    result = plan_appointment_slot(timeline, window)
    assert result[0] == False

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1), st.tuples(st.integers(), st.integers()))
def test_timeline_update(timeline, window):
    assume(window[0] < window[1])
    result = plan_appointment_slot(timeline, window)
    assert result[0] == True