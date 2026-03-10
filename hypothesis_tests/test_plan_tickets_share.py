import math
from hypothesis import given, assume, strategies as st

def plan_tickets_share(total, weights, *, floor_to_int=True, minimum=0):
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

# Property: weights_required_error_raised
@given(st.just([]))
def test_weights_required_error_raised(weights):
    try:
        plan_tickets_share(100, weights)
    except ValueError as e:
        assert str(e) == "weights required"

# Property: negative_total_error_raised
@given(st.integers(max_value=-1))
def test_negative_total_error_raised(total):
    try:
        plan_tickets_share(total, [10, 20, 30])
    except ValueError as e:
        assert str(e) == "negative total"

# Property: negative_minimum_error_raised
@given(st.integers(max_value=-1))
def test_negative_minimum_error_raised(minimum):
    try:
        plan_tickets_share(100, [10, 20, 30], minimum=minimum)
    except ValueError as e:
        assert str(e) == "negative minimum"

# Property: zero_total_weight_error_raised
@given(st.lists(st.integers(), min_size=1).filter(lambda x: sum(x) == 0))
def test_zero_total_weight_error_raised(weights):
    try:
        plan_tickets_share(100, weights)
    except ValueError as e:
        assert str(e) == "zero total weight"

# Property: floor_to_int_enabled
@given(st.lists(st.integers()), st.booleans())
def test_floor_to_int_enabled(weights, floor_to_int):
    result = plan_tickets_share(100, weights, floor_to_int=floor_to_int)
    if floor_to_int:
        assert all(isinstance(x, int) for x in result)
    else:
        assert all(isinstance(x, float) for x in result)