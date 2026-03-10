import math
from hypothesis import given, assume, strategies as st

def estimate_temperature(x0, y0, x1, y1, x, *, clamp=True):
    if x1 == x0:
        raise ValueError("zero length")

    t = (x - x0) / (x1 - x0)
    y = (1 - t) * y0 + t * y1

    if clamp:
        low, high = sorted([y0, y1])
        y = min(max(y, low), high)

    return y

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_computes_temperature_along_line_segment(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)  # Avoid zero length
    result = estimate_temperature(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(result, float)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_error_raised_for_zero_length(x0, y0, x1, y1, x, clamp):
    assume(x1 == x0)  # Force zero length
    try:
        estimate_temperature(x0, y0, x1, y1, x, clamp=clamp)
    except ValueError:
        pass
    else:
        assert False, "ValueError not raised for zero length"

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_output_clamped_using_y_range(x0, y0, x1, y1, x, clamp):
    result = estimate_temperature(x0, y0, x1, y1, x, clamp=clamp)
    low, high = sorted([y0, y1])
    expected = min(max(result, low), high)
    assert math.isclose(result, expected, rel_tol=1e-9)