import math
from hypothesis import given, assume, strategies as st

def audit_window_filter(timestamps, now, *, window=30):
    cutoff = now - window
    return [t for t in timestamps if t >= cutoff]

@given(st.lists(st.integers(), min_size=1), st.integers())
def test_audit_window_filter_correctness(timestamps, now):
    result = audit_window_filter(timestamps, now)
    assert all(t >= now - 30 for t in result)

@given(st.lists(st.integers(), min_size=1), st.integers())
def test_audit_window_filter_boundary_exclusion(timestamps, now):
    result = audit_window_filter(timestamps, now)
    assert all(t > now - 30 for t in result)