import math
from hypothesis import given, assume, strategies as st

def cpu_allocator(total, weights, *, minimum=0):
    if total < 0:
        raise ValueError("total must be non-negative")
    if minimum < 0:
        raise ValueError("minimum must be non-negative")
    if not weights:
        raise ValueError("no weights provided")
    if not any(weights):
        raise ValueError("all weights are zero")

    total_weight = sum(weights)
    planned = [max(minimum, (w / total_weight) * total) for w in weights]

    allocations = [int(x) for x in planned]
    return allocations

@given(st.integers(max_value=-1))  # Generator: negative integer for total
def test_cpu_allocator_valid_input_check(total):
    try:
        cpu_allocator(total, [1, 2, 3])
    except ValueError as e:
        assert "total must be non-negative" in str(e)

@given(st.integers(max_value=0))  # Generator: zero for minimum
def test_cpu_allocator_valid_minimum_check(minimum):
    try:
        cpu_allocator(10, [1, 2, 3], minimum=minimum)
    except ValueError as e:
        assert "minimum must be non-negative" in str(e)

@given(st.lists(st.integers(), min_size=0, max_size=0))  # Generator: empty list for weights
def test_cpu_allocator_non_empty_weights_check(weights):
    try:
        cpu_allocator(10, weights)
    except ValueError as e:
        assert "no weights provided" in str(e)

@given(st.lists(st.integers(), min_size=1).filter(lambda x: all(val == 0 for val in x)))  # Generator: list with all zeros
def test_cpu_allocator_non_zero_weights_check(weights):
    try:
        cpu_allocator(10, weights)
    except ValueError as e:
        assert "all weights are zero" in str(e)

@given(st.lists(st.integers(), min_size=1), st.integers(min_value=0))  # Generator: non-empty list of integers for weights and minimum
def test_cpu_allocator_allocation_calculation(weights, minimum):
    assume(sum(weights) > 0)
    allocations = cpu_allocator(100, weights, minimum=minimum)
    assert sum(allocations) == 100

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(min_value=0.0))  # Generator: non-empty list of floats for weights and minimum
def test_cpu_allocator_truncation_bug(weights, minimum):
    assume(sum(weights) > 0)
    allocations = cpu_allocator(100, weights, minimum=minimum)
    assert sum(allocations) == 100  # Check if total allocation is correct

    total_weight = sum(weights)
    expected_allocations = [max(minimum, (w / total_weight) * 100) for w in weights]
    for expected, actual in zip(expected_allocations, allocations):
        assert math.isclose(expected, actual, rel_tol=1e-9)  # Check if allocations are close to expected values