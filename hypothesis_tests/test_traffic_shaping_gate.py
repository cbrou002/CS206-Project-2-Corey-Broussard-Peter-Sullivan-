import math
from hypothesis import given, assume, strategies as st

def traffic_shaping_gate(timestamps, now, *, window=10, limit=5):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]

    if len(active) > limit:
        return False, 0
    return True, limit - len(active)

@given(st.lists(st.integers(), min_size=0, max_size=5))  # Generator: list of integers with max size 5
def test_traffic_shaping_gate_list_length_limit(timestamps):
    now = 15
    result, remaining_limit = traffic_shaping_gate(timestamps, now)
    assert (result == False and remaining_limit == 0) or (result == True and remaining_limit >= 0)

@given(st.lists(st.integers(), min_size=0, max_size=10))  # Generator: list of integers with max size 10
def test_traffic_shaping_gate_list_length_no_limit(timestamps):
    now = 15
    result, remaining_limit = traffic_shaping_gate(timestamps, now)
    assert (result == True and remaining_limit >= 0)

@given(st.lists(st.integers(), min_size=0, max_size=5))  # Generator: list of integers with max size 5
def test_traffic_shaping_gate_list_length_block_traffic(timestamps):
    now = 15
    result, remaining_limit = traffic_shaping_gate(timestamps, now)
    assert result == False

@given(st.lists(st.integers(), min_size=0, max_size=10))  # Generator: list of integers with max size 10
def test_traffic_shaping_gate_list_length_allow_traffic(timestamps):
    now = 15
    result, remaining_limit = traffic_shaping_gate(timestamps, now)
    assert result == True