import math
from hypothesis import given, strategies as st

def adjust_allocation(current, target, *, damping=0.7):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    updated = []
    for idx in range(len(current)):
        updated.append(current[idx] + (target[idx] - current[idx]) * damping)

    return updated

@given(st.lists(st.floats(), min_size=1), st.lists(st.floats(), min_size=1), st.floats())
def test_adjust_allocation_shape_mismatch(current, target, damping):
    assume(len(current) != len(target))
    try:
        adjust_allocation(current, target, damping=damping)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(), min_size=1), st.lists(st.floats(), min_size=1), st.floats())
def test_adjust_allocation_empty_allocation(current, target, damping):
    assume(not current)
    try:
        adjust_allocation(current, target, damping=damping)
    except ValueError as e:
        assert str(e) == "empty allocation"

@given(st.lists(st.floats(), min_size=1), st.lists(st.floats(), min_size=1), st.floats())
def test_adjust_allocation_updates_allocation_weights(current, target, damping):
    updated = adjust_allocation(current, target, damping=damping)
    for idx in range(len(current)):
        assert math.isclose(updated[idx], current[idx] + (target[idx] - current[idx]) * damping, rel_tol=1e-9)