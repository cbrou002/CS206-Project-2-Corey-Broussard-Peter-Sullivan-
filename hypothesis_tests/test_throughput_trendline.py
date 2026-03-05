import math
from hypothesis import given, strategies as st

def throughput_trendline(x0, y0, x1, y1, x, *, clamp=True):
    if x1 == x0:
        raise ValueError("zero length")
    t = (x - x0) / (x1 - x0)
    y = (1 - t) * y0 + t * y1
    if clamp:
        low, high = sorted([y0, y1])
        y = min(max(y, low), high)
    return y

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_computes_throughput_along_line_segment(x0, y0, x1, y1, x, clamp):
    assume(x1 != x0)  # Avoid zero length
    result = throughput_trendline(x0, y0, x1, y1, x, clamp=clamp)
    assert isinstance(result, float)

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_zero_length_exception_raised(x0, y0, x1, y1, x):
    assume(x1 == x0)  # Trigger zero length exception
    try:
        throughput_trendline(x0, y0, x1, y1, x)
    except ValueError:
        pass
    else:
        assert False, "Exception not raised"

@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_output_clamped_within_y_range(x0, y0, x1, y1, x):
    result = throughput_trendline(x0, y0, x1, y1, x, clamp=True)
    low, high = sorted([y0, y1])
    assert low <= result <= high