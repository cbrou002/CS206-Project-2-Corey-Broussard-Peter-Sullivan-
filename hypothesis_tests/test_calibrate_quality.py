import math
from hypothesis import given, assume, strategies as st

def calibrate_quality(x0, y0, x1, y1, x, *, clamp=True):
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
def test_calibrate_quality_linear_estimate(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)  # Avoid degenerate segment
    assume((x >= min(x0, x1)) and (x <= max(x0, x1)))  # Ensure x is within the range
    assume((y0 != y1) or (x0 == x1))  # Avoid division by zero

    expected_y = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
    result = calibrate_quality(x0, y0, x1, y1, x, clamp=clamp)

    assert math.isclose(result, expected_y, rel_tol=1e-9)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_calibrate_quality_clamp_values(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)  # Avoid degenerate segment
    assume((x >= min(x0, x1)) and (x <= max(x0, x1)))  # Ensure x is within the range
    assume((y0 != y1) or (x0 == x1))  # Avoid division by zero

    result = calibrate_quality(x0, y0, x1, y1, x, clamp=clamp)

    if clamp:
        assert result >= min(y0, y1)
        assert result <= max(y0, y1)
    else:
        assert result == y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)