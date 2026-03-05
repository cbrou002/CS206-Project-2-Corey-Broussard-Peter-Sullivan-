import math
from hypothesis import given, assume, strategies as st

def bandwidth_rebalance(current, target, *, damping=0.7):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    updated = []
    for idx in range(len(current)):
        updated.append(current[idx] + (target[idx] - current[idx]) * damping)

    return updated

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False, max_value=1000), min_size=1))
def test_shape_mismatch_check(current, target):
    assume(len(current) != len(target))
    try:
        bandwidth_rebalance(current, target)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_empty_allocation_check(current):
    assume(not current)
    try:
        bandwidth_rebalance(current, [0.0])
    except ValueError as e:
        assert str(e) == "empty allocation"