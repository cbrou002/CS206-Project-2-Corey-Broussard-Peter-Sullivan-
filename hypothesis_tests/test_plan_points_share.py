import math
from hypothesis import given, assume, strategies as st

def plan_points_share(total, weights, *, minimum=0):
    """
    Distribute points allotment across lanes.
    """
    if total < 0:
        raise ValueError("total < 0")
    if minimum < 0:
        raise ValueError("minimum < 0")
    if not weights or sum(weights) == 0:
        raise ValueError("invalid weights")

    weight_sum = sum(weights)
    def compute_share(w):
        raw = (w / weight_sum) * total
        return raw if raw >= minimum else minimum

    shares = list(map(compute_share, weights))
    # BUG: integer conversion discards fractional remainder.
    return list(map(int, shares))

@given(st.integers(min_value=0))
def test_valid_total(total):
    assume(total < 0)
    try:
        plan_points_share(total, [1, 2, 3])
    except ValueError as e:
        assert str(e) == "total < 0"

@given(st.integers(max_value=-1))
def test_invalid_total(total):
    assume(total >= 0)
    try:
        plan_points_share(total, [1, 2, 3])
    except ValueError as e:
        assert str(e) != "total < 0"

@given(st.integers(min_value=0))
def test_valid_minimum(minimum):
    assume(minimum < 0)
    try:
        plan_points_share(10, [1, 2, 3], minimum=minimum)
    except ValueError as e:
        assert str(e) == "minimum < 0"

@given(st.integers(max_value=-1))
def test_invalid_minimum(minimum):
    assume(minimum >= 0)
    try:
        plan_points_share(10, [1, 2, 3], minimum=minimum)
    except ValueError as e:
        assert str(e) != "minimum < 0"

@given(st.lists(st.integers(), min_size=1))
def test_non_empty_weights(weights):
    assume(not weights or sum(weights) == 0)
    try:
        plan_points_share(10, weights)
    except ValueError as e:
        assert str(e) == "invalid weights"