import math
from hypothesis import given, assume, strategies as st

def calibrate_loss(x0, y0, x1, y1, x, *, clamp=True):
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
def test_linear_estimate_loss(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)  # Avoid degenerate segment
    assume(not math.isclose(x0, x1, rel_tol=1e-9))  # Avoid degenerate segment

    result = calibrate_loss(x0, y0, x1, y1, x, clamp=clamp)

    assert isinstance(result, float)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_clamp_values(x0, y0, x1, y1, x, clamp):
    assume(clamp)  # Clamping enabled

    result = calibrate_loss(x0, y0, x1, y1, x, clamp=clamp)

    assert isinstance(result, float)
    assert min(y0, y1) <= result <= max(y0, y1)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_no_clamping(x0, y0, x1, y1, x, clamp):
    assume(not clamp)  # Clamping disabled

    result = calibrate_loss(x0, y0, x1, y1, x, clamp=clamp)

    assert isinstance(result, float)
    assert y0 <= result <= y1

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_clamp_lower_bound(x0, y0, x1, y1, x, clamp):
    assume(clamp)  # Clamping enabled
    assume(y0 < y1)  # Ensure y0 is lower than y1

    result = calibrate_loss(x0, y0, x1, y1, x, clamp=clamp)

    assert isinstance(result, float)
    assert result >= min(y0, y1)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_clamp_upper_bound(x0, y0, x1, y1, x, clamp):
    assume(clamp)  # Clamping enabled
    assume(y0 < y1)  # Ensure y0 is lower than y1

    result = calibrate_loss(x0, y0, x1, y1, x, clamp=clamp)

    assert isinstance(result, float)
    assert result <= max(y0, y1)