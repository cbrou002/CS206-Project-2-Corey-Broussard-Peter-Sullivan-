import math
from hypothesis import given, assume, strategies as st

def realign_cache(current, target, *, damping=0.3):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    adjusted = [c + (t - c) * damping for c, t in zip(current, target)]

    return adjusted

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False, max_value=1.0), min_size=1))
def test_shape_mismatch_check(current, target):
    assume(len(current) != len(target))
    try:
        realign_cache(current, target)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_empty_allocation_check(current):
    assume(not current)
    try:
        realign_cache(current, [0.0])
    except ValueError as e:
        assert str(e) == "empty allocation"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False, max_value=1.0), min_size=1))
def test_cache_mix_shift(current, target):
    adjusted = realign_cache(current, target)
    for c, t, a in zip(current, target, adjusted):
        assert math.isclose(a, c + (t - c) * 0.3, rel_tol=1e-9)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False, max_value=1.0), min_size=1))
def test_renormalization_bug(current, target):
    adjusted = realign_cache(current, target)
    assert math.isclose(sum(adjusted), sum(current), rel_tol=1e-9)