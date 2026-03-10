import math
from hypothesis import given, strategies as st, assume

def rating_curve(x0, y0, x1, y1, x, *, clamp=True):
    if x1 == x0:
        raise ValueError("zero length")
    t = (x - x0) / (x1 - x0)
    y = (1 - t) * y0 + t * y1
    if clamp:
        low, high = sorted([y0, y1])
        y = min(max(y, low), high)
    return y

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_rating_curve_computes_rating_along_line_segment(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)
    result = rating_curve(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(result, float)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_rating_curve_zero_length_exception_raised(x0, y0, x1, y1, x):
    assume(x1 == x0)
    try:
        rating_curve(x0, y0, x1, y1, x)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for zero length but none was raised"

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_rating_curve_output_clamped_within_y_range(x0, y0, x1, y1, x, clamp):
    low, high = min(y0, y1), max(y0, y1)
    assume(clamp is True)
    result = rating_curve(x0, y0, x1, y1, x, clamp=clamp)
    assert low <= result <= high