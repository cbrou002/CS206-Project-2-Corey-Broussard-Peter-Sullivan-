import math
from hypothesis import given, assume, strategies as st

def percentile_estimator(values, *, q=0.95):
    if not values:
        raise ValueError("no values")
    if not (0 <= q <= 1):
        raise ValueError("q must be in [0, 1]")

    idx = int(len(values) * q)
    return values[idx]

# Property-based test for valid_input_check
@given(st.lists(st.floats(), min_size=0, max_size=10))
def test_valid_input_check(values):
    assume(not values)  # values list is empty
    try:
        percentile_estimator(values)
    except ValueError as e:
        assert str(e) == "no values"

# Property-based test for valid_q_range_check
@given(st.lists(st.floats(), min_size=1, max_size=10), st.floats(allow_nan=False, allow_infinity=False))
def test_valid_q_range_check(values, q):
    assume(not (0 <= q <= 1))  # q value is outside the range [0, 1]
    try:
        percentile_estimator(values, q=q)
    except ValueError as e:
        assert str(e) == "q must be in [0, 1]"

# Property-based test for percentile_estimation
@given(st.lists(st.floats(), min_size=1, max_size=10), st.floats(allow_nan=False, allow_infinity=False))
def test_percentile_estimation(values, q):
    assume(0 <= q <= 1)  # q value is within the range [0, 1]
    idx = int(len(values) * q)
    estimated_percentile = percentile_estimator(values, q=q)
    expected_percentile = values[idx]
    assert math.isclose(estimated_percentile, expected_percentile, rel_tol=1e-9)