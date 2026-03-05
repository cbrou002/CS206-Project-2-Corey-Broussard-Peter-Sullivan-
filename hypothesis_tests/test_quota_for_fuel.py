import math
from hypothesis import given, assume, strategies as st

def quota_for_fuel(total, weights, *, minimum=0):
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

@given(st.integers(max_value=-1))  # Generator: negative total
def test_valid_total_negative(total):
    try:
        quota_for_fuel(total, [1, 2, 3])
    except ValueError as e:
        assert "total must be non-negative" in str(e)

@given(st.integers(max_value=0))  # Generator: zero total
def test_valid_total_zero(total):
    try:
        quota_for_fuel(total, [1, 2, 3])
    except ValueError as e:
        assert "total must be non-negative" in str(e)

@given(st.integers(max_value=0))  # Generator: zero minimum
def test_valid_minimum_zero(minimum):
    try:
        quota_for_fuel(10, [1, 2, 3], minimum=minimum)
    except ValueError as e:
        assert "minimum must be non-negative" in str(e)

@given(st.lists(st.integers(), min_size=0, max_size=0))  # Generator: empty weights list
def test_non_empty_weights_empty(weights):
    try:
        quota_for_fuel(10, weights)
    except ValueError as e:
        assert "no weights provided" in str(e)

@given(st.lists(st.integers(), min_size=1).filter(lambda x: all(val == 0 for val in x)))  # Generator: all weights are zero
def test_non_zero_weights_all_zero(weights):
    try:
        quota_for_fuel(10, weights)
    except ValueError as e:
        assert "all weights are zero" in str(e)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_allocation_truncation_bug(weights):
    assume(sum(weights) != 0)
    allocations = quota_for_fuel(100, weights)
    assert sum(allocations) == 100  # Total allocation should sum up to the total fuel units

    # Check if any leftover units are lost due to truncation
    assert sum(allocations) == sum([int(x) for x in [max(0, (w / sum(weights)) * 100) for w in weights]])  # Redistribution check

    # Additional checks can be added to verify the redistribution of leftover units