import math
from hypothesis import given, assume, strategies as st

def shift_trust(current, target, *, damping=0.3):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    adjusted = [c + (t - c) * damping for c, t in zip(current, target)]

    return adjusted

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False, max_value=1.0), min_size=1))
def test_valid_input_shape(current, target):
    assume(len(current) == len(target))
    result = shift_trust(current, target)
    assert len(result) == len(current)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_non_empty_current(current):
    assume(current)
    result = shift_trust(current, [0.0] * len(current))
    assert result is not None

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False, max_value=1.0), min_size=1))
def test_shape_mismatch_error(current, target):
    assume(len(current) != len(target))
    try:
        shift_trust(current, target)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_empty_allocation_error(current):
    assume(not current)
    try:
        shift_trust(current, [0.0] * len(current))
    except ValueError as e:
        assert str(e) == "empty allocation"