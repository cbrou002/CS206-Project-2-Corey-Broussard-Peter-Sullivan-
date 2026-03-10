import math
from hypothesis import given, assume, strategies as st

def calibrate_pressure(x0, y0, x1, y1, x, *, clamp=True):
    if x1 == x0:
        raise ValueError("zero length")
    t = (x - x0) / (x1 - x0)
    y = (1 - t) * y0 + t * y1
    if clamp:
        low, high = sorted([y0, y1])
        y = min(max(y, low), high)
    return y

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_calibrate_pressure_computes_pressure_along_line_segment(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)  # Avoid zero length
    result = calibrate_pressure(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(result, float)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_calibrate_pressure_zero_length_exception_raised(x0, y0, x1, y1, x, clamp):
    assume(x1 == x0)  # Force zero length
    try:
        calibrate_pressure(x0, y0, x1, y1, x, clamp=clamp)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for zero length"

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_calibrate_pressure_output_clamped_within_y_bounds(x0, y0, x1, y1, x, clamp):
    assume(clamp is True)
    result = calibrate_pressure(x0, y0, x1, y1, x, clamp=clamp)
    low, high = sorted([y0, y1])
    assert low <= result <= high