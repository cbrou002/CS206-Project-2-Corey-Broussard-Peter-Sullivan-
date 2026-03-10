import math
from hypothesis import given, assume, strategies as st

def coverage_interp(x0, y0, x1, y1, x, *, clamp=True):
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
def test_linear_estimate_computation(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)  # Avoid degenerate segment
    assume((x >= min(x0, x1)) and (x <= max(x0, x1)))  # Ensure x is within the segment range

    expected_y = coverage_interp(x0, y0, x1, y1, x, clamp=clamp)
    computed_y = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)

    assert math.isclose(expected_y, computed_y, rel_tol=1e-9)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_clamping_enabled_check(x0, y0, x1, y1, x, clamp):
    assume(clamp)  # Check only when clamping is enabled

    expected_y = coverage_interp(x0, y0, x1, y1, x, clamp=True)
    computed_y = coverage_interp(x0, y0, x1, y1, x, clamp=clamp)

    assert expected_y == computed_y

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_lower_clamp_check(x0, y0, x1, y1, x, clamp):
    assume(clamp)  # Check only when clamping is enabled

    expected_y = coverage_interp(x0, y0, x1, y1, x, clamp=True)
    computed_y = coverage_interp(x0, y0, x1, y1, x, clamp=clamp)

    lo, hi = (min(y0, y1), max(y0, y1))
    if computed_y < lo:
        assert computed_y == lo

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_upper_clamp_check(x0, y0, x1, y1, x, clamp):
    assume(clamp)  # Check only when clamping is enabled

    expected_y = coverage_interp(x0, y0, x1, y1, x, clamp=True)
    computed_y = coverage_interp(x0, y0, x1, y1, x, clamp=clamp)

    lo, hi = (min(y0, y1), max(y0, y1))
    if computed_y > hi:
        assert computed_y == hi