import math
from hypothesis import given, assume, strategies as st

def batchnorm_running_mean(current_mean, batch_mean, *, momentum=0.9):
    if not (0 <= momentum <= 1):
        raise ValueError("momentum must be in [0, 1]")
    return (1 - momentum) * current_mean + momentum * batch_mean

@given(st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6), 
       st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
       st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6))
def test_batchnorm_running_mean_valid_momentum_range(current_mean, batch_mean, momentum):
    assume(0 <= momentum <= 1)
    result = batchnorm_running_mean(current_mean, batch_mean, momentum=momentum)
    expected = (1 - momentum) * current_mean + momentum * batch_mean
    assert math.isclose(result, expected, rel_tol=1e-9)

@given(st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6), 
       st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
       st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=-1e-6).filter(lambda x: x < 0 or x > 1))
def test_batchnorm_running_mean_momentum_check(current_mean, batch_mean, momentum):
    assume(not 0 <= momentum <= 1)
    try:
        batchnorm_running_mean(current_mean, batch_mean, momentum=momentum)
        assert False, "Expected ValueError for invalid momentum"
    except ValueError:
        assert True