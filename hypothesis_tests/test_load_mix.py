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

@given(st.lists(st.floats(), min_size=1), st.lists(st.floats(), min_size=1))
def test_shape_mismatch(current, target):
    assume(len(current) != len(target))
    try:
        load_mix(current, target)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(), min_size=1))
def test_empty_allocation(current):
    assume(not current)
    try:
        load_mix(current, [0.0])
    except ValueError as e:
        assert str(e) == "empty allocation"