import math
from hypothesis import given, assume, strategies as st

def budget_mix(current, target, *, damping=0.3):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    adjusted = [c + (t - c) * damping for c, t in zip(current, target)]

    return adjusted

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_budget_mix_shape_mismatch_exception(current, target, damping):
    assume(len(current) != len(target))
    try:
        budget_mix(current, target, damping=damping)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_budget_mix_empty_allocation_exception(current, damping):
    assume(not current)
    try:
        budget_mix(current, [0.0], damping=damping)
    except ValueError as e:
        assert str(e) == "empty allocation"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_budget_mix_list_comprehension(current, target, damping):
    adjusted = budget_mix(current, target, damping=damping)
    assert len(adjusted) == len(current)
    for adj, c, t in zip(adjusted, current, target):
        expected = c + (t - c) * damping
        assert math.isclose(adj, expected, rel_tol=1e-9)