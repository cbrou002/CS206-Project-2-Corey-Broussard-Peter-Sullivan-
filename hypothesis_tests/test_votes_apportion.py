import math
from hypothesis import given, assume, strategies as st

def votes_apportion(total, weights, *, floor_to_int=True, minimum=0):
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

# Property: raises_exception_weights_required
@given(st.lists(st.floats(), min_size=0, max_size=0))
def test_raises_exception_weights_required(weights):
    try:
        votes_apportion(100, weights)
    except ValueError as e:
        assert str(e) == "weights required"

# Property: raises_exception_negative_total
@given(st.integers(max_value=-1))
def test_raises_exception_negative_total(total):
    try:
        votes_apportion(total, [1, 2, 3])
    except ValueError as e:
        assert str(e) == "negative total"

# Property: raises_exception_negative_minimum
@given(st.integers(max_value=-1))
def test_raises_exception_negative_minimum(minimum):
    try:
        votes_apportion(100, [1, 2, 3], minimum=minimum)
    except ValueError as e:
        assert str(e) == "negative minimum"

# Property: raises_exception_zero_total_weight
@given(st.lists(st.floats(), min_size=1).filter(lambda x: sum(x) == 0))
def test_raises_exception_zero_total_weight(weights):
    try:
        votes_apportion(100, weights)
    except ValueError as e:
        assert str(e) == "zero total weight"

# Property: returns_list_of_integers
@given(st.lists(st.floats(), min_size=1), st.booleans())
def test_returns_list_of_integers(weights, floor_to_int):
    result = votes_apportion(100, weights, floor_to_int=floor_to_int)
    assert all(isinstance(x, int) for x in result)

# Property: returns_list_of_floats
@given(st.lists(st.floats(), min_size=1), st.booleans())
def test_returns_list_of_floats(weights, floor_to_int):
    result = votes_apportion(100, weights, floor_to_int=floor_to_int)
    assert all(isinstance(x, float) for x in result)