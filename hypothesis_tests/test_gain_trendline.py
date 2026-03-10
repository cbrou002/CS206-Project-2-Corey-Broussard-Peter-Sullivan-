import math
from hypothesis import given, strategies as st

def gain_trendline(x0, y0, x1, y1, x, *, clamp=True):
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

# Property-based tests

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_linear_estimate_computation(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)  # Avoid degenerate segment
    assume(x >= min(x0, x1) and x <= max(x0, x1))  # Ensure x is within the range
    expected_y = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
    assert math.isclose(gain_trendline(x0, y0, x1, y1, x, clamp=clamp), expected_y, rel_tol=1e-9)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_clamp_option_usage(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)  # Avoid degenerate segment
    assume(x >= min(x0, x1) and x <= max(x0, x1))  # Ensure x is within the range
    computed_y = gain_trendline(x0, y0, x1, y1, x, clamp=clamp)
    if clamp:
        assert computed_y >= min(y0, y1) and computed_y <= max(y0, y1)
    else:
        assert computed_y == y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_clamp_bug_fix(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)  # Avoid degenerate segment
    assume(x >= min(x0, x1) and x <= max(x0, x1))  # Ensure x is within the range
    computed_y = gain_trendline(x0, y0, x1, y1, x, clamp=clamp)
    if clamp:
        assert computed_y >= min(y0, y1) and computed_y <= max(y0, y1)
    else:
        assert computed_y == y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)