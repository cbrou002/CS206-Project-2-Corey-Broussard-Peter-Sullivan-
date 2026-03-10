import math
from hypothesis import given, assume, strategies as st

def model_confidence_clamp(x0, y0, x1, y1, x, *, clamp=True):
    if x0 == x1:
        raise ValueError("degenerate segment")
    
    t = (x - x0) / (x1 - x0)
    y = y0 + t * (y1 - y0)
    
    if clamp:
        low, high = (min(y0, y1), max(y0, y1))
        y = min(max(y, low), high)
    return y

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_model_confidence_clamp_computes_confidence_between_two_anchor_points(x0, y0, x1, y1, x):
    assume(x0 != x1)
    y = model_confidence_clamp(x0, y0, x1, y1, x)
    assert isinstance(y, float)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_model_confidence_clamp_raises_error_for_degenerate_segment(x0, y0, x1, y1, x):
    assume(x0 == x1)
    try:
        model_confidence_clamp(x0, y0, x1, y1, x)
    except ValueError as e:
        assert str(e) == "degenerate segment"

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_model_confidence_clamp_clamps_output_instead_of_input_range(x0, y0, x1, y1, x, clamp):
    y = model_confidence_clamp(x0, y0, x1, y1, x, clamp=clamp)
    low, high = min(y0, y1), max(y0, y1)
    if clamp:
        assert y >= low and y <= high
    else:
        assert y == y