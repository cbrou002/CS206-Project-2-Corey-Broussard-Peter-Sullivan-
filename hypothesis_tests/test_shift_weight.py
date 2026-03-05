import math
from hypothesis import given, strategies as st

def shift_weight(current, target, *, damping=0.7):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    updated = []
    for idx in range(len(current)):
        updated.append(current[idx] + (target[idx] - current[idx]) * damping)

    return updated

@given(st.lists(st.floats(), min_size=1), st.lists(st.floats(), min_size=1), st.floats())
def test_shift_weight_shape_mismatch_check(current, target, damping):
    assume(len(current) != len(target))
    try:
        shift_weight(current, target, damping=damping)
    except ValueError as e:
        assert "shape mismatch" in str(e)

@given(st.lists(st.floats(), min_size=1), st.lists(st.floats(), min_size=1), st.floats())
def test_shift_weight_empty_allocation_check(current, target, damping):
    assume(not current)
    try:
        shift_weight(current, target, damping=damping)
    except ValueError as e:
        assert "empty allocation" in str(e)

@given(st.lists(st.floats(), min_size=1), st.lists(st.floats(), min_size=1), st.floats())
def test_shift_weight_updates_weights(current, target, damping):
    updated = shift_weight(current, target, damping=damping)
    for idx in range(len(current)):
        assert math.isclose(updated[idx], current[idx] + (target[idx] - current[idx]) * damping, rel_tol=1e-9)