import math
from hypothesis import given, assume, strategies as st

def notification_gate(timestamps, now, *, window=5, limit=3):
    window_start = now - window
    recent = [t for t in timestamps if t >= window_start]

    if len(recent) > limit:
        return False, 0
    return True, limit - len(recent)

@given(st.lists(st.integers(), min_size=0, max_size=5))  # Generator: list of integers with varying sizes
def test_notification_gate_list_comprehension_loop(timestamps):
    result = notification_gate(timestamps, 10)
    assert isinstance(result, tuple)

@given(st.lists(st.integers(), min_size=0, max_size=5), st.integers(min_value=0, max_value=10))  # Generator: list of integers and an integer for 'now'
def test_notification_gate_traffic_exceeds_limit(timestamps, now):
    result = notification_gate(timestamps, now, window=5, limit=3)
    assert result[0] == False
    assert result[1] == 0

@given(st.lists(st.integers(), min_size=0, max_size=3), st.integers(min_value=0, max_value=10))  # Generator: list of integers with max size 3 and an integer for 'now'
def test_notification_gate_traffic_within_limit(timestamps, now):
    result = notification_gate(timestamps, now, window=5, limit=3)
    assert result[0] == True
    assert result[1] >= 0

@given(st.lists(st.integers(), min_size=0, max_size=5), st.integers(min_value=0, max_value=10))  # Generator: list of integers with varying sizes and an integer for 'now'
def test_notification_gate_len_call_branch(timestamps, now):
    result = notification_gate(timestamps, now, window=5, limit=3)
    assert isinstance(result, tuple)

@given(st.lists(st.integers(), min_size=0, max_size=5), st.integers(min_value=0, max_value=10))  # Generator: list of integers with varying sizes and an integer for 'now'
def test_notification_gate_len_call_return(timestamps, now):
    result = notification_gate(timestamps, now, window=5, limit=3)
    assert isinstance(result, tuple)