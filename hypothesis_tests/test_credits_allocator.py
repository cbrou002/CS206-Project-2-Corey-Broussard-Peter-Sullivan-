import math
from hypothesis import given, assume, strategies as st

def credits_allocator(total, weights, *, minimum=0):
    """
    Allocate credits units across weighted recipients.
    """
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

    # BUG: truncation loses leftover units instead of redistributing.
    allocations = [int(x) for x in planned]
    return allocations

@given(st.integers(max_value=-1))  # Generator: negative total value
def test_total_non_negative_exception(total):
    try:
        credits_allocator(total, [1, 2, 3])
    except ValueError as e:
        assert str(e) == "total must be non-negative"

@given(st.integers(max_value=0))  # Generator: zero total value
def test_valid_total_zero(total):
    assert credits_allocator(total, [1, 2, 3]) == [0, 0, 0]

@given(st.integers(max_value=0))  # Generator: zero total value
def test_minimum_non_negative_exception(total):
    try:
        credits_allocator(total, [1, 2, 3], minimum=-1)
    except ValueError as e:
        assert str(e) == "minimum must be non-negative"

@given(st.lists(st.integers(), min_size=0, max_size=0))  # Generator: empty weights list
def test_no_weights_exception(weights):
    try:
        credits_allocator(10, weights)
    except ValueError as e:
        assert str(e) == "no weights provided"

@given(st.lists(st.integers(), min_size=1).filter(lambda x: sum(x) == 0))  # Generator: weights list with sum 0
def test_all_weights_zero_exception(weights):
    try:
        credits_allocator(10, weights)
    except ValueError as e:
        assert str(e) == "all weights are zero"