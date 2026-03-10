import math
from hypothesis import given, assume, strategies as st

def shift_risk(current, target, *, damping=0.3):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    adjusted = [c + (t - c) * damping for c, t in zip(current, target)]

    return adjusted

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_shift_risk_shape_mismatch_check(current, target, damping):
    assume(len(current) != len(target))
    try:
        shift_risk(current, target, damping=damping)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_shift_risk_empty_allocation_check(current, target, damping):
    assume(not current)
    try:
        shift_risk(current, target, damping=damping)
    except ValueError as e:
        assert str(e) == "empty allocation"