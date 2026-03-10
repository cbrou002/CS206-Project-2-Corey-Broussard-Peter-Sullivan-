import math
from hypothesis import given, assume, strategies as st

def lru_evictor(order, *, capacity):
    if capacity < 0:
        raise ValueError("capacity must be non-negative")
    while len(order) > capacity:
        order.pop(0)
    return order

@given(st.lists(st.integers(), min_size=0), st.integers())
def test_capacity_non_negative(order, capacity):
    assume(capacity < 0)
    try:
        lru_evictor(order, capacity=capacity)
    except ValueError as e:
        assert str(e) == "capacity must be non-negative"

@given(st.lists(st.integers(), min_size=0), st.integers(min_value=0))
def test_eviction_condition(order, capacity):
    assume(len(order) > capacity)
    result = lru_evictor(order, capacity=capacity)
    assert len(result) <= capacity

@given(st.lists(st.integers(), min_size=0), st.integers(min_value=0))
def test_eviction_loop(order, capacity):
    assume(len(order) > capacity)
    result = lru_evictor(order, capacity=capacity)
    assert len(result) <= capacity