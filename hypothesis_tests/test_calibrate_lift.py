import math
from hypothesis import given, assume, strategies as st

def calibrate_lift(x0, y0, x1, y1, x, *, clamp=True):
    if x1 == x0:
        raise ValueError("zero length")

    t = (x - x0) / (x1 - x0)
    y = (1 - t) * y0 + t * y1

    if clamp:
        low, high = sorted([y0, y1])
        y = min(max(y, low), high)

    return y

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_calibrate_lift_computes_lift_along_line_segment(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)  # Ensure x1 is not equal to x0
    result = calibrate_lift(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(result, float)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_calibrate_lift_zero_length_exception_raised(x0, y0, x1, y1, x, clamp):
    assume(x1 == x0)  # Ensure x1 is equal to x0
    try:
        calibrate_lift(x0, y0, x1, y1, x, clamp=clamp)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError to be raised"

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_calibrate_lift_output_clamped_using_y_range(x0, y0, x1, y1, x, clamp):
    assume(clamp)  # Ensure clamp is True
    result = calibrate_lift(x0, y0, x1, y1, x, clamp=clamp)
    low, high = sorted([y0, y1])
    assert low <= result <= high