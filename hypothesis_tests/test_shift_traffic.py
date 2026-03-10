import math
from hypothesis import given, strategies as st

def shift_traffic(current, target, *, damping=0.7):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    updated = []
    for idx in range(len(current)):
        updated.append(current[idx] + (target[idx] - current[idx]) * damping)

    return updated

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_shift_traffic_shape_mismatch_check(current, target, damping):
    assume(len(current) != len(target))
    try:
        shift_traffic(current, target, damping=damping)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_shift_traffic_empty_allocation_check(current, damping):
    assume(not current)
    try:
        shift_traffic(current, [0.0], damping=damping)
    except ValueError as e:
        assert str(e) == "empty allocation"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_shift_traffic_updates_values(current, target, damping):
    updated = shift_traffic(current, target, damping=damping)
    for idx in range(len(current)):
        assert math.isclose(updated[idx], current[idx] + (target[idx] - current[idx]) * damping, rel_tol=1e-9)