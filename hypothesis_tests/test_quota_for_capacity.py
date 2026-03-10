import math
from hypothesis import given, assume, strategies as st

def quota_for_capacity(total, weights, *, floor_to_int=True, minimum=0):
    """
    Compute weighted allocation for capacity capacity.
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

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_quota_for_capacity_no_zero_sum(weights):
    assume(sum(weights) != 0)
    result = quota_for_capacity(100, weights)
    assert sum(result) == 100

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_quota_for_capacity_floor_to_int(weights):
    assume(sum(weights) != 0)
    result = quota_for_capacity(100, weights, floor_to_int=True)
    assert all(isinstance(x, int) for x in result)