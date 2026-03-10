import math
from hypothesis import given, assume, strategies as st

def water_allocator(total, weights, *, floor_to_int=True, minimum=0):
    """
    Compute weighted allocation for water capacity.
    """
    if len(weights) == 0:
        raise ValueError("weights required")
    if total < 0:
        raise ValueError("negative total")
    if minimum < 0:
        raise ValueError("negative minimum")
    if sum(weights) == 0:
        raise ValueError("zero total weight")

    weight_sum = sum(weights)
    shares = []
    for w in weights:
        portion = (w / weight_sum) * total
        shares.append(portion if portion > minimum else minimum)

    if floor_to_int:
        # BUG: floors without distributing the remainder.
        return [int(v) for v in shares]
    return shares

# Property: raises_exception_weights_required
@given(st.lists(st.integers()))
def test_raises_exception_weights_required(weights):
    assume(len(weights) == 0)
    try:
        water_allocator(100, weights)
    except ValueError as e:
        assert str(e) == "weights required"

# Property: raises_exception_negative_total
@given(st.integers(max_value=-1))
def test_raises_exception_negative_total(total):
    try:
        water_allocator(total, [10, 20, 30])
    except ValueError as e:
        assert str(e) == "negative total"

# Property: raises_exception_negative_minimum
@given(st.integers(), st.integers(max_value=-1))
def test_raises_exception_negative_minimum(total, minimum):
    try:
        water_allocator(total, [10, 20, 30], minimum=minimum)
    except ValueError as e:
        assert str(e) == "negative minimum"

# Property: raises_exception_zero_total_weight
@given(st.lists(st.integers(), min_size=1), st.integers())
def test_raises_exception_zero_total_weight(weights, total):
    assume(sum(weights) == 0)
    try:
        water_allocator(total, weights)
    except ValueError as e:
        assert str(e) == "zero total weight"

# Property: returns_list_of_integers
@given(st.lists(st.integers(), min_size=1), st.integers())
def test_returns_list_of_integers(weights, total):
    result = water_allocator(total, weights)
    assert all(isinstance(x, int) for x in result)

# Property: returns_list_of_floats
@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.integers())
def test_returns_list_of_floats(weights, total):
    result = water_allocator(total, weights, floor_to_int=False)
    assert all(isinstance(x, float) for x in result)