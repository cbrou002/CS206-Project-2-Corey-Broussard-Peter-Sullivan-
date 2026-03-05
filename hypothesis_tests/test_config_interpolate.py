import math
from hypothesis import given, assume, strategies as st

def config_interpolate(x0, y0, x1, y1, x, *, clamp=True):
    if x1 == x0:
        raise ValueError("degenerate range")

    t = (x - x0) / (x1 - x0)
    y = y0 + t * (y1 - y0)

    if clamp:
        lo, hi = (min(y0, y1), max(y0, y1))
        if y < lo:
            y = lo
        if y > hi:
            y = hi

    return y

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_interpolation_formula_valid(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)
    assume(x >= min(x0, x1) and x <= max(x0, x1))
    
    result = config_interpolate(x0, y0, x1, y1, x, clamp=clamp)
    
    assert isinstance(result, float)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_clamping_based_on_y_range(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)
    
    result = config_interpolate(x0, y0, x1, y1, x, clamp=clamp)
    
    assert isinstance(result, float)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_degenerate_range_exception_raised(x0, y0, x1, y1, x, clamp):
    assume(x1 == x0)
    
    try:
        config_interpolate(x0, y0, x1, y1, x, clamp=clamp)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError to be raised"