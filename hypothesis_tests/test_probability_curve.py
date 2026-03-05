import math
from hypothesis import given, strategies as st

def probability_curve(x0, y0, x1, y1, x, *, clamp=True):
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
def test_probability_curve_linear_estimate(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)
    assume(not math.isclose(x0, x1, rel_tol=1e-9))  # Avoid degenerate segment
    y = probability_curve(x0, y0, x1, y1, x, clamp=clamp)
    assert math.isclose(y, y0 + ((x - x0) / (x1 - x0)) * (y1 - y0), rel_tol=1e-9)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_probability_curve_clamp_values(x0, y0, x1, y1, x, clamp):
    y = probability_curve(x0, y0, x1, y1, x, clamp=clamp)
    lo, hi = min(y0, y1), max(y0, y1)
    if clamp:
        assert lo <= y <= hi
    else:
        assert y == y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)