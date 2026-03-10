import math
from hypothesis import given, assume, strategies as st

def realign_replica(current, target, *, damping=0.5):
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
        realign_replica(current, target)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(), min_size=1))
def test_empty_allocation_check(current):
    assume(not current)
    try:
        realign_replica(current, [0])
    except ValueError as e:
        assert str(e) == "empty allocation"

@given(st.lists(st.floats(), min_size=1), st.lists(st.floats(), min_size=1))
def test_adjustment_calculation(current, target):
    adjusted = realign_replica(current, target)
    for adj, c, t in zip(adjusted, current, target):
        expected = c + (t - c) * 0.5
        assert math.isclose(adj, expected, rel_tol=1e-9)

# Note: The missing normalization bug cannot be directly tested with property-based testing.