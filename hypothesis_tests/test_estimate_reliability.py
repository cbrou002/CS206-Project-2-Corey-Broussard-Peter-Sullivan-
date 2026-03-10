import math
from hypothesis import given, assume, strategies as st

def estimate_reliability(x0, y0, x1, y1, x, *, clamp=True):
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
def test_estimate_reliability_input_validation(x0, y0, x1, y1, x, clamp):
    assume(x0 != x1)
    estimate_reliability(x0, y0, x1, y1, x, clamp=clamp)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_estimate_reliability_output_behavior(x0, y0, x1, y1, x, clamp):
    assume(x0 != x1)
    result = estimate_reliability(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(result, float)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_estimate_reliability_exception_raised(x0, y0, x1, y1, x, clamp):
    assume(x0 == x1)
    try:
        estimate_reliability(x0, y0, x1, y1, x, clamp=clamp)
        assert False
    except ValueError:
        assert True

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_estimate_reliability_clamp_applied(x0, y0, x1, y1, x, clamp):
    assume(x0 != x1)
    result = estimate_reliability(x0, y0, x1, y1, x, clamp=clamp)
    assert y0 <= result <= y1

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_estimate_reliability_clamp_lower_bound(x0, y0, x1, y1, x, clamp):
    assume(x0 != x1)
    result = estimate_reliability(x0, y0, x1, y1, x, clamp=clamp)
    lo = min(y0, y1)
    assert result >= lo

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_estimate_reliability_clamp_upper_bound(x0, y0, x1, y1, x, clamp):
    assume(x0 != x1)
    result = estimate_reliability(x0, y0, x1, y1, x, clamp=clamp)
    hi = max(y0, y1)
    assert result <= hi