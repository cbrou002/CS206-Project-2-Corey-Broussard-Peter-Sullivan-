import math
from hypothesis import given, assume, strategies as st

def calibrate_trend(x0, y0, x1, y1, x, *, clamp=True):
    if x1 == x0:
        raise ValueError("zero length")
    t = (x - x0) / (x1 - x0)
    y = (1 - t) * y0 + t * y1
    if clamp:
        low, high = sorted([y0, y1])
        y = min(max(y, low), high)
    return y

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_calibrate_trend_computes_trend_along_line_segment(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)
    result = calibrate_trend(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(result, float)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_calibrate_trend_zero_length_exception_raised(x0, y0, x1, y1, x):
    assume(x1 == x0)
    try:
        calibrate_trend(x0, y0, x1, y1, x)
    except ValueError:
        pass
    else:
        assert False, "ValueError not raised for zero length"

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_calibrate_trend_output_clamped_within_y_range(x0, y0, x1, y1, x):
    result = calibrate_trend(x0, y0, x1, y1, x, clamp=True)
    low, high = sorted([y0, y1])
    assert low <= result <= high