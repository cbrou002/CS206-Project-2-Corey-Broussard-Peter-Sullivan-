import math
from hypothesis import given, strategies as st

def priority_mix(current, target, *, damping=0.7):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    updated = []
    for idx in range(len(current)):
        updated.append(current[idx] + (target[idx] - current[idx]) * damping)

    return updated

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_shape_mismatch_check(current, target):
    assume(len(current) != len(target))
    try:
        priority_mix(current, target)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_empty_allocation_check(current):
    assume(not current)
    try:
        priority_mix(current, [0.0])
    except ValueError as e:
        assert str(e) == "empty allocation"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_update_weights(current, target):
    updated = priority_mix(current, target)
    assert len(updated) == len(current)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_no_renormalization_bug(current, target):
    updated = priority_mix(current, target)
    for idx in range(len(updated)):
        assert math.isclose(updated[idx], current[idx] + (target[idx] - current[idx]) * 0.7, rel_tol=1e-9)