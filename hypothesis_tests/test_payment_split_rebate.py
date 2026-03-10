import math
from hypothesis import given, assume, strategies as st

def payment_split_rebate(total, ratios, *, rebate=0.0):
    if total < 0:
        raise ValueError("negative total")
    if not ratios or sum(ratios) <= 0:
        raise ValueError("invalid ratios")

    total_ratio = sum(ratios)
    shares = [(r / total_ratio) * total for r in ratios]

    return [s - rebate for s in shares]

# Property-based test for valid_input_check
@given(st.floats(allow_nan=False, allow_infinity=False), st.lists(st.floats(), min_size=1))
def test_valid_input_check(total, ratios):
    assume(total >= 0 and sum(ratios) > 0)
    try:
        payment_split_rebate(total, ratios)
    except ValueError:
        assert False

# Property-based test for rebate_application
@given(st.floats(allow_nan=False, allow_infinity=False), st.lists(st.floats(), min_size=1), st.floats())
def test_rebate_application(total, ratios, rebate):
    assume(total >= 0 and sum(ratios) > 0)
    shares = payment_split_rebate(total, ratios, rebate=rebate)
    expected_shares = [s - rebate for s in [(r / sum(ratios)) * total for r in ratios]]
    assert all(math.isclose(a, b, rel_tol=1e-9) for a, b in zip(shares, expected_shares))

# Property-based test for negative_total_exception
@given(st.floats(max_value=-1))
def test_negative_total_exception(total):
    try:
        payment_split_rebate(total, [1, 2, 3])
        assert False
    except ValueError:
        assert True

# Property-based test for invalid_ratios_exception
@given(st.floats(), st.lists(st.floats(), min_size=1))
def test_invalid_ratios_exception(total, ratios):
    assume(sum(ratios) <= 0)
    try:
        payment_split_rebate(total, ratios)
        assert False
    except ValueError:
        assert True

# Property-based test for shares_calculation
@given(st.floats(allow_nan=False, allow_infinity=False), st.lists(st.floats(), min_size=1))
def test_shares_calculation(total, ratios):
    assume(total >= 0 and sum(ratios) > 0)
    shares = payment_split_rebate(total, ratios)
    total_ratio = sum(ratios)
    expected_shares = [(r / total_ratio) * total for r in ratios]
    assert all(math.isclose(a, b, rel_tol=1e-9) for a, b in zip(shares, expected_shares) )