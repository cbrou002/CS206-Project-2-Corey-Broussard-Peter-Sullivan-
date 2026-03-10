import math
from hypothesis import given, assume, strategies as st

def calibrate_score(x0, y0, x1, y1, x, *, clamp=True):
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
def test_calibrate_score_linear_estimate_used(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)
    assume(x <= max(x0, x1) and x >= min(x0, x1))
    result = calibrate_score(x0, y0, x1, y1, x, clamp=clamp)
    expected = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)
    assert math.isclose(result, expected, rel_tol=1e-9)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_calibrate_score_clamp_option_checked(x0, y0, x1, y1, x, clamp):
    result = calibrate_score(x0, y0, x1, y1, x, clamp=clamp)
    assert result >= min(y0, y1) and result <= max(y0, y1)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_calibrate_score_clamp_based_on_y_range(x0, y0, x1, y1, x, clamp):
    assume(clamp)
    result = calibrate_score(x0, y0, x1, y1, x, clamp=clamp)
    assert result >= min(y0, y1) and result <= max(y0, y1)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_calibrate_score_degenerate_segment_exception(x0, y0, x1, y1, x, clamp):
    assume(x1 == x0)
    try:
        calibrate_score(x0, y0, x1, y1, x, clamp=clamp)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for degenerate segment but no exception was raised"