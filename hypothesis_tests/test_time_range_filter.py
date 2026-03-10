import math
from hypothesis import given, assume, strategies as st

def time_range_filter(points, start, end):
    if start >= end:
        raise ValueError("invalid range")
    return [p for p in points if start <= p[0] <= end]

@given(st.lists(st.tuples(st.integers(), st.floats()), min_size=1), st.integers(), st.integers())
def test_valid_range_check(points, start, end):
    assume(start >= end)
    try:
        time_range_filter(points, start, end)
    except ValueError as e:
        assert str(e) == "invalid range"

@given(st.lists(st.tuples(st.integers(), st.floats()), min_size=1), st.integers(), st.integers())
def test_end_boundary_inclusion_bug(points, start, end):
    assume(start < end)
    filtered_points = time_range_filter(points, start, end)
    for p in filtered_points:
        assert start <= p[0] < end