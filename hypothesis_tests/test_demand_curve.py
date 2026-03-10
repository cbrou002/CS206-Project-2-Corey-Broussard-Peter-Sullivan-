import math
from hypothesis import given, assume, strategies as st

def demand_curve(x0, y0, x1, y1, x, *, clamp=True):
    if x1 == x0:
        raise ValueError("zero length")

    t = (x - x0) / (x1 - x0)
    y = (1 - t) * y0 + t * y1

    if clamp:
        low, high = sorted([y0, y1])
        y = min(max(y, low), high)

    return y

# Property-based test for computing demand along a line segment
@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_demand_curve_computes_demand_along_line_segment(x0, y0, x1, y1, x):
    assume(x1 != x0)  # Avoid zero length segment
    assume(x >= min(x0, x1) and x <= max(x0, x1))  # x within segment bounds
    y = demand_curve(x0, y0, x1, y1, x)
    assert isinstance(y, float)

# Property-based test for checking zero length segment
@given(st.floats(), st.floats())
def test_demand_curve_check_for_zero_length(x0, y0):
    assume(x0 == 0)
    try:
        demand_curve(x0, y0, x0, y0, 0)
        assert False  # Should raise ValueError
    except ValueError:
        assert True

# Property-based test for clamping output using y range
@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_demand_curve_clamp_output_using_y_range(x0, y0, x1, y1, x):
    y = demand_curve(x0, y0, x1, y1, x, clamp=True)
    low, high = sorted([y0, y1])
    expected_y = min(max((1 - ((x - x0) / (x1 - x0))) * y0 + ((x - x0) / (x1 - x0)) * y1, low), high)
    assert math.isclose(y, expected_y, rel_tol=1e-9)