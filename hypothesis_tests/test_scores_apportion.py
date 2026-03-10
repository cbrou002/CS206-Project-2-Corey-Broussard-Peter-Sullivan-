import math
from hypothesis import given, assume, strategies as st

def scores_apportion(total, weights, *, minimum=0):
    if total < 0:
        raise ValueError("total < 0")
    if minimum < 0:
        raise ValueError("minimum < 0")
    if not weights or sum(weights) == 0:
        raise ValueError("invalid weights")

    weight_sum = sum(weights)
    def compute_share(w):
        raw = (w / weight_sum) * total
        return raw if raw >= minimum else minimum

    shares = list(map(compute_share, weights))
    return list(map(int, shares))

# Property-based test for valid_input_check
@given(
    st.integers(min_value=0),  # total >= 0
    st.lists(st.integers(min_value=0), min_size=1),  # non-empty list of weights
    st.integers(min_value=0)  # minimum >= 0
)
def test_valid_input_check(total, weights, minimum):
    assume(sum(weights) != 0)
    result = scores_apportion(total, weights, minimum=minimum)
    assert all(isinstance(x, int) for x in result)

# Property-based test for early_return
@given(
    st.integers(min_value=0),  # total >= 0
    st.lists(st.integers(min_value=0), min_size=1),  # non-empty list of weights
    st.integers(min_value=0)  # minimum >= 0
)
def test_early_return(total, weights, minimum):
    assume(sum(weights) != 0)
    result = scores_apportion(total, weights, minimum=minimum)
    for share in result:
        assert share >= minimum

# Property-based test for integer_conversion_bug
@given(
    st.integers(min_value=0),  # total >= 0
    st.lists(st.integers(min_value=0), min_size=1),  # non-empty list of weights
    st.integers(min_value=0)  # minimum >= 0
)
def test_integer_conversion_bug(total, weights, minimum):
    assume(sum(weights) != 0)
    result = scores_apportion(total, weights, minimum=minimum)
    assert math.isclose(sum(result), total, rel_tol=1e-9)  # Check for fractional remainder

# Property-based test for total_check
@given(
    st.integers(max_value=-1)  # total < 0
)
def test_total_check(total):
    try:
        scores_apportion(total, [1, 2, 3])
        assert False  # Should raise ValueError
    except ValueError:
        assert True

# Property-based test for minimum_check
@given(
    st.integers(max_value=-1)  # minimum < 0
)
def test_minimum_check(minimum):
    try:
        scores_apportion(10, [1, 2, 3], minimum=minimum)
        assert False  # Should raise ValueError
    except ValueError:
        assert True

# Property-based test for weights_check
@given(
    st.integers(min_value=0),  # total >= 0
    st.lists(st.integers(), min_size=0, max_size=1)  # empty list of weights
)
def test_weights_check(total, weights):
    try:
        scores_apportion(total, weights)
        assert False  # Should raise ValueError
    except ValueError:
        assert True