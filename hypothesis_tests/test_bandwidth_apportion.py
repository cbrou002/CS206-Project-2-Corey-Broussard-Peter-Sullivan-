import math
from hypothesis import given, assume, strategies as st

def bandwidth_apportion(total, weights, *, minimum=0):
    if total < 0:
        raise ValueError("total must be non-negative")
    if minimum < 0:
        raise ValueError("minimum must be non-negative")
    if not weights or sum(weights) == 0:
        raise ValueError("invalid weights")

    total_weight = sum(weights)
    raw = [max(minimum, (w / total_weight) * total) for w in weights]

    return [int(x) for x in raw]

# Property-based test for valid_input_check
@given(
    st.floats(allow_nan=False, allow_infinity=False, min_value=0), 
    st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), 
    st.integers(min_value=0)
)
def test_valid_input_check(total, weights, minimum):
    assume(total >= 0)
    assume(minimum >= 0)
    assume(weights and sum(weights) != 0)
    
    result = bandwidth_apportion(total, weights, minimum=minimum)
    assert all(isinstance(x, int) for x in result)

# Property-based test for integer_truncation_bug
@given(
    st.floats(allow_nan=False, allow_infinity=False, min_value=0), 
    st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), 
    st.integers(min_value=0)
)
def test_integer_truncation_bug(total, weights, minimum):
    assume(total >= 0)
    assume(minimum >= 0)
    assume(weights and sum(weights) != 0)
    
    result = bandwidth_apportion(total, weights, minimum=minimum)
    assert math.isclose(sum(result), total, rel_tol=1e-9)