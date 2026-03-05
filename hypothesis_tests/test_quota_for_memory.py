import math
from hypothesis import given, assume, strategies as st

def quota_for_memory(total, weights, *, minimum=0):
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

@given(st.integers(max_value=-1))  # total < 0
def test_quota_for_memory_negative_total(total):
    try:
        quota_for_memory(total, [1, 2, 3])
    except ValueError as e:
        assert str(e) == "total must be non-negative"

@given(st.integers(), st.integers(max_value=-1))  # minimum < 0
def test_quota_for_memory_negative_minimum(total, minimum):
    try:
        quota_for_memory(total, [1, 2, 3], minimum=minimum)
    except ValueError as e:
        assert str(e) == "minimum must be non-negative"

@given(st.lists(st.integers(), min_size=1))  # not weights
def test_quota_for_memory_no_weights(weights):
    try:
        quota_for_memory(10, weights)
    except ValueError as e:
        assert str(e) == "no weights provided"

@given(st.lists(st.integers(), min_size=1, max_size=3).filter(lambda x: sum(x) == 0))  # all weights are zero
def test_quota_for_memory_all_weights_zero(weights):
    try:
        quota_for_memory(10, weights)
    except ValueError as e:
        assert str(e) == "all weights are zero"