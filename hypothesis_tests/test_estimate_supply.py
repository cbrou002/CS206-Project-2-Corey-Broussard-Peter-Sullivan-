import math
from hypothesis import given, assume, strategies as st

def estimate_supply(x0, y0, x1, y1, x, *, clamp=True):
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
def test_linear_estimate(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)  # Avoid degenerate segment
    assume(not math.isclose(x0, x1))  # Avoid degenerate segment
    assume(not math.isclose(y0, y1))  # Avoid degenerate segment

    estimated_y = estimate_supply(x0, y0, x1, y1, x, clamp=clamp)

    if clamp:
        lo, hi = min(y0, y1), max(y0, y1)
        if y0 <= y1:
            assert lo <= estimated_y <= hi
        else:
            assert hi <= estimated_y <= lo
    else:
        assert y0 <= estimated_y <= y1 or y1 <= estimated_y <= y0

# Additional tests for other properties can be added here if needed.