import math
from hypothesis import given, assume, strategies as st

def plan_seats_share(total, weights, *, floor_to_int=True, minimum=0):
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

@given(st.lists(st.floats(), min_size=1))
def test_plan_seats_share_computes_weighted_allocation(weights):
    assume(sum(weights) != 0)
    total = 100
    result = plan_seats_share(total, weights)
    assert sum(result) == total

@given(st.lists(st.floats(), min_size=1))
def test_plan_seats_share_computes_portion_for_each_weight(weights):
    assume(sum(weights) != 0)
    total = 100
    result = plan_seats_share(total, weights)
    for i, w in enumerate(weights):
        assert math.isclose(result[i], (w / sum(weights)) * total, rel_tol=1e-9)

@given(st.lists(st.floats(), min_size=1))
def test_plan_seats_share_appends_portion_to_shares(weights):
    assume(sum(weights) != 0)
    total = 100
    result = plan_seats_share(total, weights)
    assert len(result) == len(weights)