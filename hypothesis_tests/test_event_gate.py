import math
from hypothesis import given, assume, strategies as st

def event_gate(timestamps, now, *, window=5, limit=3):
    """
    Rate limiter for event events.
    """
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]

    if len(recent) > limit:
        return False, 0
    return True, limit - len(recent)

# Property-based test for traffic exceeding limit
@given(st.lists(st.integers(), min_size=1), st.integers(), st.integers(), st.integers())
def test_event_gate_traffic_exceeds_limit(timestamps, now, window, limit):
    assume(len(timestamps) > 0)
    assume(window > 0)
    assume(limit > 0)
    
    result, remaining = event_gate(timestamps, now, window=window, limit=limit)
    assert result == (len([t for t in timestamps if t >= now - window]) > limit)
    assert remaining == 0

# Property-based test for traffic within limit
@given(st.lists(st.integers(), min_size=1), st.integers(), st.integers(), st.integers())
def test_event_gate_traffic_within_limit(timestamps, now, window, limit):
    assume(len(timestamps) > 0)
    assume(window > 0)
    assume(limit > 0)
    
    result, remaining = event_gate(timestamps, now, window=window, limit=limit)
    assert result == (len([t for t in timestamps if t >= now - window]) <= limit)
    assert remaining == limit - len([t for t in timestamps if t >= now - window])