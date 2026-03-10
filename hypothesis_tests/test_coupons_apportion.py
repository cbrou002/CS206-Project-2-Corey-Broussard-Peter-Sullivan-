import math
from hypothesis import given, assume, strategies as st

def coupons_apportion(total, weights, *, floor_to_int=True, minimum=0):
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
        return [int(v) for v in shares]
    return shares

# Property: raises_value_error_weights_required
@given(st.lists(st.floats(), min_size=0, max_size=0))
def test_weights_required_empty_list(weights):
    try:
        coupons_apportion(100, weights)
    except ValueError as e:
        assert str(e) == "weights required"

# Property: raises_value_error_negative_total
@given(st.floats(max_value=-0.1))
def test_negative_total(total):
    try:
        coupons_apportion(total, [1, 2, 3])
    except ValueError as e:
        assert str(e) == "negative total"

# Property: raises_value_error_negative_minimum
@given(st.floats(), st.floats(max_value=-0.1))
def test_negative_minimum(total, minimum):
    try:
        coupons_apportion(total, [1, 2, 3], minimum=minimum)
    except ValueError as e:
        assert str(e) == "negative minimum"

# Property: raises_value_error_zero_total_weight
@given(st.lists(st.floats(), min_size=1), st.floats())
def test_zero_total_weight(weights, total):
    assume(sum(weights) == 0)
    try:
        coupons_apportion(total, weights)
    except ValueError as e:
        assert str(e) == "zero total weight"

# Property: returns_list_of_integers
@given(st.lists(st.floats(), min_size=1), st.floats())
def test_returns_list_of_integers(weights, total):
    result = coupons_apportion(total, weights)
    assert all(isinstance(x, int) for x in result)

# Property: returns_list_of_floats
@given(st.lists(st.floats(), min_size=1), st.floats())
def test_returns_list_of_floats(weights, total):
    result = coupons_apportion(total, weights, floor_to_int=False)
    assert all(isinstance(x, float) for x in result)