import math
from hypothesis import given, assume, strategies as st

def quota_for_storage(total, weights, *, minimum=0):
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
def test_total_negative_error(total):
    try:
        quota_for_storage(total, [1, 2, 3])
    except ValueError as e:
        assert str(e) == "total must be non-negative"

@given(st.integers(max_value=0))  # minimum < 0
def test_minimum_negative_error(minimum):
    try:
        quota_for_storage(10, [1, 2, 3], minimum=minimum)
    except ValueError as e:
        assert str(e) == "minimum must be non-negative"

@given(st.lists(st.integers(), min_size=0, max_size=0))  # empty weights
def test_empty_weights_error(weights):
    try:
        quota_for_storage(10, weights)
    except ValueError as e:
        assert str(e) == "no weights provided"

@given(st.lists(st.integers(), min_size=1).filter(lambda x: all(val == 0 for val in x)))  # all weights are zero
def test_zero_weights_error(weights):
    try:
        quota_for_storage(10, weights)
    except ValueError as e:
        assert str(e) == "all weights are zero"