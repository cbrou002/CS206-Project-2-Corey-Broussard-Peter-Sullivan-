import math
from hypothesis import given, assume, strategies as st

def demand_forecast_curve(x0, y0, x1, y1, x, *, clamp=True):
    if x0 == x1:
        raise ValueError("x0 == x1")

    ratio = (x - x0) / (x1 - x0)
    y = y0 + ratio * (y1 - y0)

    if clamp:
        low, high = (min(y0, y1), max(y0, y1))
        if y < low:
            y = low
        elif y > high:
            y = high
    return y

# Property-based test for linear_interpolation_used
@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_linear_interpolation_used(x0, y0, x1, y1, x):
    assume(x0 != x1)
    assume(x0 <= x <= x1)
    y = demand_forecast_curve(x0, y0, x1, y1, x)
    assert math.isclose(y, y0 + ((x - x0) / (x1 - x0)) * (y1 - y0), rel_tol=1e-9)

# Property-based test for x0_not_equal_x1
@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats())
def test_x0_not_equal_x1(x0, y0, x1, y1, x):
    assume(x0 == x1)
    try:
        demand_forecast_curve(x0, y0, x1, y1, x)
    except ValueError as e:
        assert str(e) == "x0 == x1"

# Property-based test for clamp_applied
@given(st.floats(), st.floats(), st.floats(), st.floats(), st.floats(), st.booleans())
def test_clamp_applied(x0, y0, x1, y1, x, clamp):
    y = demand_forecast_curve(x0, y0, x1, y1, x, clamp=clamp)
    low, high = min(y0, y1), max(y0, y1)
    if clamp:
        assert low <= y <= high
    else:
        assert y == y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)