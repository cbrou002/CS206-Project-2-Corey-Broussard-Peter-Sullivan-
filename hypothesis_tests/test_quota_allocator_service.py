import math
from hypothesis import given, assume, strategies as st

def quota_allocator_service(total, weights, *, minimum=0):
    if total < 0:
        raise ValueError("total must be non-negative")
    if minimum < 0:
        raise ValueError("minimum must be non-negative")
    if not weights or sum(weights) == 0:
        raise ValueError("invalid weights")

    weight_sum = sum(weights)
    raw = [max(minimum, (w / weight_sum) * total) for w in weights]

    return [int(x) for x in raw]

# Property-based tests

@given(st.integers(max_value=-1))  # Generator: negative integer (Branch: total < 0)
def test_quota_allocator_service_total_check(total):
    try:
        quota_allocator_service(total, [1, 2, 3])
    except ValueError as e:
        assert "total must be non-negative" in str(e)

@given(st.integers(max_value=-1))  # Generator: negative integer (Branch: total < 0)
def test_quota_allocator_service_minimum_check(total):
    try:
        quota_allocator_service(10, [1, 2, 3], minimum=total)
    except ValueError as e:
        assert "minimum must be non-negative" in str(e)

@given(st.lists(st.integers(), min_size=1).filter(lambda x: sum(x) == 0))  # Generator: list with sum 0 (Branch: sum(weights) == 0)
def test_quota_allocator_service_weights_check(weights):
    try:
        quota_allocator_service(10, weights)
    except ValueError as e:
        assert "invalid weights" in str(e)

@given(st.lists(st.floats(), min_size=1), st.floats(allow_nan=False, allow_infinity=False))  # Generator: non-empty list of floats, float
def test_quota_allocator_service_list_comprehension_1(weights, total):
    assume(total >= 0)
    assume(all(w >= 0 for w in weights))
    result = quota_allocator_service(total, weights)
    assert sum(result) == total

@given(st.lists(st.floats(), min_size=1), st.floats(allow_nan=False, allow_infinity=False))  # Generator: non-empty list of floats, float
def test_quota_allocator_service_list_comprehension_2(weights, total):
    assume(total >= 0)
    assume(all(w >= 0 for w in weights))
    result = quota_allocator_service(total, weights)
    assert all(isinstance(x, int) for x in result)