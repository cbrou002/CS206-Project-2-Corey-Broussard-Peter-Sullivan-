import math
from hypothesis import given, assume, strategies as st

def adjust_supply(current, target, *, damping=0.7):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    updated = []
    for idx in range(len(current)):
        updated.append(current[idx] + (target[idx] - current[idx]) * damping)

    return updated

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_adjust_supply_shape_mismatch_check(current, target, damping):
    assume(len(current) != len(target))
    try:
        adjust_supply(current, target, damping=damping)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_adjust_supply_empty_allocation_check(current, target, damping):
    assume(not current)
    try:
        adjust_supply(current, target, damping=damping)
    except ValueError as e:
        assert str(e) == "empty allocation"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_adjust_supply_updates_weights(current, target, damping):
    updated = adjust_supply(current, target, damping=damping)
    for idx in range(len(current)):
        assert math.isclose(updated[idx], current[idx] + (target[idx] - current[idx]) * damping, rel_tol=1e-9)