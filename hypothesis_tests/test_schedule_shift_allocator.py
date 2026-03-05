import math
from hypothesis import given, assume, strategies as st

def schedule_shift_allocator(total, weights, *, minimum=0):
    if total < 0:
        raise ValueError("total must be non-negative")
    if minimum < 0:
        raise ValueError("minimum must be non-negative")
    if not weights or sum(weights) == 0:
        raise ValueError("invalid weights")

    weight_sum = sum(weights)
    shares = [max(minimum, (w / weight_sum) * total) for w in weights]

    return [int(x) for x in shares]

# Property: valid_total_non_negative
@given(st.integers(max_value=-1))
def test_valid_total_non_negative(total):
    try:
        schedule_shift_allocator(total, [1, 2, 3])
    except ValueError as e:
        assert "total must be non-negative" in str(e)

# Property: valid_minimum_non_negative
@given(st.lists(st.integers()), st.integers(max_value=-1))
def test_valid_minimum_non_negative(weights, minimum):
    try:
        schedule_shift_allocator(10, weights, minimum=minimum)
    except ValueError as e:
        assert "minimum must be non-negative" in str(e)

# Property: valid_weights_non_empty
@given(st.lists(st.integers(min_value=1), min_size=1))
def test_valid_weights_non_empty(weights):
    try:
        schedule_shift_allocator(10, weights)
    except ValueError as e:
        assert "invalid weights" in str(e)

# Property: valid_shares_calculation
@given(st.lists(st.integers(min_value=1), min_size=1), st.integers(min_value=1))
def test_valid_shares_calculation(weights, total):
    shares = schedule_shift_allocator(total, weights)
    assert sum(shares) == total

# Property: valid_shares_integer_conversion
@given(st.lists(st.floats(min_value=0, allow_nan=False, allow_infinity=False), min_size=1), st.integers(min_value=1))
def test_valid_shares_integer_conversion(weights, total):
    shares = schedule_shift_allocator(total, weights)
    assert all(isinstance(x, int) for x in shares)