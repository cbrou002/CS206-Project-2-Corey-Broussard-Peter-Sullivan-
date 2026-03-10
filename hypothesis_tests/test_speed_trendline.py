import math
from hypothesis import given, assume, strategies as st

def speed_trendline(x0, y0, x1, y1, x, *, clamp=True):
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

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_speed_trendline_valid_input_check(x0, y0, x1, y1, x, clamp):
    assume(x0 != x1)
    assume(x0 <= x1)
    result = speed_trendline(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(result, (int, float))

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_speed_trendline_clamp_option(x0, y0, x1, y1, x, clamp):
    result = speed_trendline(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(result, (int, float))

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_speed_trendline_clamp_using_y_bounds_lower(x0, y0, x1, y1, x, clamp):
    assume(clamp)
    assume(y0 < y1)
    result = speed_trendline(x0, y0, x1, y1, x, clamp=clamp)
    assert result >= y0

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_speed_trendline_clamp_using_y_bounds_upper(x0, y0, x1, y1, x, clamp):
    assume(clamp)
    assume(y0 < y1)
    result = speed_trendline(x0, y0, x1, y1, x, clamp=clamp)
    assert result <= y1