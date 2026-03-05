import math
from hypothesis import given, assume, strategies as st

def confidence_trendline(x0, y0, x1, y1, x, *, clamp=True):
    if x0 == x1:
        raise ValueError("x0 equals x1")

    ratio = (x - x0) / (x1 - x0)
    y = y0 + ratio * (y1 - y0)

    if clamp:
        lo, hi = (min(y0, y1), max(y0, y1))
        if y < lo:
            y = lo
        elif y > hi:
            y = hi

    return y

# Property: The function interpolates a confidence value based on the input parameters.
@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_interpolates_confidence_value(x0, y0, x1, y1, x):
    result = confidence_trendline(x0, y0, x1, y1, x)
    assert isinstance(result, float)

# Property: The function raises a ValueError if x0 is equal to x1.
@given(st.floats())
def test_raises_value_error_when_x0_equals_x1(x):
    assume(x != 0)  # Avoid division by zero
    try:
        confidence_trendline(x, 0, x, 1, 0)
    except ValueError:
        pass
    else:
        assert False

# Property: If clamp is True, the interpolated value is clamped within the y0 and y1 bounds.
@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_clamps_interpolated_value_within_y_bounds(x0, y0, x1, y1, x, clamp):
    result = confidence_trendline(x0, y0, x1, y1, x, clamp=clamp)
    assert y0 <= result <= y1

# Property: If clamp is False, the interpolated value is not clamped.
@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_does_not_clamp_interpolated_value_when_clamp_is_false(x0, y0, x1, y1, x):
    result = confidence_trendline(x0, y0, x1, y1, x, clamp=False)
    assert y0 <= result <= y1 or math.isclose(result, y0, rel_tol=1e-9) or math.isclose(result, y1, rel_tol=1e-9)