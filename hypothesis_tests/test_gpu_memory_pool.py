import math
from hypothesis import given, assume, strategies as st

def gpu_memory_pool(allocations, request, *, capacity):
    if capacity <= 0:
        raise ValueError("capacity must be positive")
    if request < 0:
        raise ValueError("request must be non-negative")

    used = sum(allocations)

    if used + request > capacity:
        return False
    return True

@given(st.lists(st.integers(min_value=0), min_size=1), st.integers(min_value=0), st.integers(min_value=1))
def test_gpu_memory_pool_capacity_positive(allocations, request, capacity):
    assume(capacity <= 0)
    try:
        gpu_memory_pool(allocations, request, capacity=capacity)
    except ValueError as e:
        assert str(e) == "capacity must be positive"

@given(st.lists(st.integers(min_value=0), min_size=1), st.integers(max_value=-1), st.integers(min_value=1))
def test_gpu_memory_pool_request_non_negative(allocations, request, capacity):
    assume(request < 0)
    try:
        gpu_memory_pool(allocations, request, capacity=capacity)
    except ValueError as e:
        assert str(e) == "request must be non-negative"

@given(st.lists(st.integers(min_value=0), min_size=1), st.integers(min_value=0), st.integers(min_value=1))
def test_gpu_memory_pool_return_false(allocations, request, capacity):
    assume(sum(allocations) + request > capacity)
    assert gpu_memory_pool(allocations, request, capacity=capacity) == False

@given(st.lists(st.integers(min_value=0), min_size=1), st.integers(min_value=0), st.integers(min_value=1))
def test_gpu_memory_pool_return_true(allocations, request, capacity):
    assume(sum(allocations) + request <= capacity)
    assert gpu_memory_pool(allocations, request, capacity=capacity) == True