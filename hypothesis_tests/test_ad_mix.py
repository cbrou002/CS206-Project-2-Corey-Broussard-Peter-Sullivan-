import math
from hypothesis import given, assume, strategies as st

def load_mix(current, target, *, damping=0.5):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    adjusted = []
    for c, t in zip(current, target):
        adjusted.append(c + (t - c) * damping)

    return adjusted

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_shape_mismatch(current, target, damping):
    assume(len(current) != len(target))
    try:
        load_mix(current, target, damping=damping)
        assert False
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_empty_allocation(current, damping):
    assume(not current)
    try:
        load_mix(current, [0], damping=damping)
        assert False
    except ValueError as e:
        assert str(e) == "empty allocation"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_normalization_missing(current, target, damping):
    adjusted = load_mix(current, target, damping=damping)
    total_current = sum(current)
    total_adjusted = sum(adjusted)
    assert math.isclose(total_current, total_adjusted, rel_tol=1e-9)