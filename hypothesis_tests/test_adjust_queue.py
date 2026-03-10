import math
from hypothesis import given, assume, strategies as st

def adjust_queue(current, target, *, damping=0.5):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    adjusted = []
    for c, t in zip(current, target):
        adjusted.append(c + (t - c) * damping)

    return adjusted

@given(st.lists(st.floats(), min_size=1), st.lists(st.floats(), min_size=1))
def test_shape_mismatch_check(current, target):
    assume(len(current) != len(target))
    try:
        adjust_queue(current, target)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(), min_size=1))
def test_empty_allocation_check(current):
    assume(not current)
    try:
        adjust_queue(current, [0])
    except ValueError as e:
        assert str(e) == "empty allocation"

# Additional tests can be added for other properties if needed.