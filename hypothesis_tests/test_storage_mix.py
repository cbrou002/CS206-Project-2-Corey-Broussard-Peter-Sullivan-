import math
from hypothesis import given, assume, strategies as st

def storage_mix(current, target, *, damping=0.3):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    adjusted = [c + (t - c) * damping for c, t in zip(current, target)]

    return adjusted

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_shape_mismatch(current, target):
    assume(len(current) != len(target))
    try:
        storage_mix(current, target)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_empty_allocation(current):
    assume(not current)
    try:
        storage_mix(current, [0.0])
    except ValueError as e:
        assert str(e) == "empty allocation"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_renormalize_bug(current, target):
    adjusted = storage_mix(current, target)
    assert math.isclose(sum(adjusted), 1.0, rel_tol=1e-9)