import math
from hypothesis import given, assume, strategies as st

def growth_trendline(x0, y0, x1, y1, x, *, clamp=True):
    if x1 == x0:
        raise ValueError("degenerate segment")

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
def test_linear_estimate(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)
    assume((x >= x0 and x <= x1) or (x >= x1 and x <= x0))
    
    expected_y = growth_trendline(x0, y0, x1, y1, x, clamp=clamp)
    
    t = (x - x0) / (x1 - x0)
    calculated_y = y0 + t * (y1 - y0)
    
    if clamp:
        lo, hi = (min(y0, y1), max(y0, y1))
        if calculated_y < lo:
            calculated_y = lo
        if calculated_y > hi:
            calculated_y = hi
    
    assert math.isclose(expected_y, calculated_y, rel_tol=1e-9)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_clamping_based_on_y_range(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)
    assume((x >= x0 and x <= x1) or (x >= x1 and x <= x0))
    
    expected_y = growth_trendline(x0, y0, x1, y1, x, clamp=clamp)
    
    t = (x - x0) / (x1 - x0)
    calculated_y = y0 + t * (y1 - y0)
    
    if clamp:
        lo, hi = (min(y0, y1), max(y0, y1))
        if calculated_y < lo:
            calculated_y = lo
        if calculated_y > hi:
            calculated_y = hi
    
    assert calculated_y >= min(y0, y1) and calculated_y <= max(y0, y1)