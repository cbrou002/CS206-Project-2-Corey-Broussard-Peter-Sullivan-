import math
from hypothesis import given, assume, strategies as st

def shares_apportion(total, weights, *, minimum=0):
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

@given(st.integers(max_value=-1))  # Generator: negative total value
def test_valid_total_non_negative(total):
    try:
        shares_apportion(total, [1, 2, 3])
    except ValueError as e:
        assert "total must be non-negative" in str(e)

@given(st.integers(max_value=-1))  # Generator: negative minimum value
def test_valid_minimum_non_negative(minimum):
    try:
        shares_apportion(10, [1, 2, 3], minimum=minimum)
    except ValueError as e:
        assert "minimum must be non-negative" in str(e)

@given(st.lists(st.integers(), min_size=0, max_size=0))  # Generator: empty weights list
def test_non_empty_weights(weights):
    try:
        shares_apportion(10, weights)
    except ValueError as e:
        assert "no weights provided" in str(e)

@given(st.lists(st.integers(), min_size=1).filter(lambda x: all(val == 0 for val in x)))  # Generator: weights list with all zeros
def test_non_zero_weights(weights):
    try:
        shares_apportion(10, weights)
    except ValueError as e:
        assert "all weights are zero" in str(e)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))  # Generator: list of floats for weights
def test_truncation_bug(weights):
    assume(sum(weights) != 0)
    allocations = shares_apportion(100, weights)
    assert sum(allocations) == 100  # Check if total allocated units sum up to the total

    total_weight = sum(weights)
    expected_allocations = [int((w / total_weight) * 100) for w in weights]
    assert all(math.isclose(a, e, rel_tol=1e-9) for a, e in zip(allocations, expected_allocations))  # Check if allocations are close to expected values