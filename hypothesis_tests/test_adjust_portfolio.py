import math
from hypothesis import given, assume, strategies as st

def adjust_portfolio(current, target, *, damping=0.5):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty allocation")

    adjusted = []
    for c, t in zip(current, target):
        adjusted.append(c + (t - c) * damping)

    return adjusted

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_input_shape_match(current, target):
    assume(len(current) == len(target))
    result = adjust_portfolio(current, target)
    assert len(result) == len(current)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_non_empty_allocation(current, target):
    assume(current)
    result = adjust_portfolio(current, target)
    assert result

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_shape_mismatch_error(current, target):
    assume(len(current) != len(target))
    try:
        adjust_portfolio(current, target)
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_empty_allocation_error(current, target):
    assume(not current)
    try:
        adjust_portfolio(current, target)
    except ValueError as e:
        assert str(e) == "empty allocation"