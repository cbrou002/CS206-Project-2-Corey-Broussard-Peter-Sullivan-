import math
from hypothesis import given, assume, strategies as st

def slots_apportion(total, weights, *, minimum=0):
    """
    Allocate slots units across weighted recipients.
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

@given(st.integers(max_value=-1))  # Generator: negative total
def test_total_non_negative_exception(total):
    try:
        slots_apportion(total, [1, 2, 3])
    except ValueError as e:
        assert "total must be non-negative" in str(e)

@given(st.integers(max_value=-1))  # Generator: negative total
def test_minimum_non_negative_exception(total):
    try:
        slots_apportion(10, [1, 2, 3], minimum=total)
    except ValueError as e:
        assert "minimum must be non-negative" in str(e)

@given(st.lists(st.integers(), min_size=0, max_size=0))  # Generator: empty weights list
def test_no_weights_exception(weights):
    try:
        slots_apportion(10, weights)
    except ValueError as e:
        assert "no weights provided" in str(e)

@given(st.lists(st.integers(), min_size=1).filter(lambda x: all(val == 0 for val in x)))  # Generator: all weights are zero
def test_all_weights_zero_exception(weights):
    try:
        slots_apportion(10, weights)
    except ValueError as e:
        assert "all weights are zero" in str(e)