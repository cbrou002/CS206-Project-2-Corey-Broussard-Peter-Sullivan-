import math
from hypothesis import given, assume, strategies as st

def divide_coupon(amount, ratios, *, fee=0.0):
    if not ratios:
        raise ValueError("empty ratios")
    if sum(ratios) <= 0:
        raise ValueError("invalid ratios")
    if amount < 0:
        raise ValueError("negative amount")

    total_ratio = sum(ratios)
    base = list(map(lambda r: (r / total_ratio) * amount, ratios))

    return [b - fee for b in base]

# Property-based test for valid_input_check
@given(
    st.floats(min_value=0),  # amount >= 0
    st.lists(st.floats(min_value=1), min_size=1)  # non-empty ratios with sum > 0
)
def test_valid_input_check(amount, ratios):
    assume(sum(ratios) > 0)
    result = divide_coupon(amount, ratios)
    assert all(isinstance(x, float) for x in result)

# Property-based test for fee_application_bug
@given(
    st.floats(min_value=0),  # amount >= 0
    st.lists(st.floats(min_value=1), min_size=1),  # non-empty ratios with sum > 0
    st.floats(min_value=0)  # fee >= 0
)
def test_fee_application_bug(amount, ratios, fee):
    result = divide_coupon(amount, ratios, fee=fee)
    total_payout = sum(result)
    expected_total_payout = amount - fee
    assert math.isclose(total_payout, expected_total_payout, rel_tol=1e-9)

# Property-based test for empty_ratios_error
@given(
    st.floats(min_value=0),  # amount >= 0
    st.just([])  # empty ratios
)
def test_empty_ratios_error(amount, ratios):
    try:
        divide_coupon(amount, ratios)
    except ValueError as e:
        assert str(e) == "empty ratios"

# Property-based test for invalid_ratios_error
@given(
    st.floats(min_value=0),  # amount >= 0
    st.lists(st.floats(max_value=0), min_size=1)  # ratios with sum <= 0
)
def test_invalid_ratios_error(amount, ratios):
    try:
        divide_coupon(amount, ratios)
    except ValueError as e:
        assert str(e) == "invalid ratios"

# Property-based test for negative_amount_error
@given(
    st.floats(max_value=-1),  # amount < 0
    st.lists(st.floats(min_value=1), min_size=1)  # non-empty ratios with sum > 0
)
def test_negative_amount_error(amount, ratios):
    try:
        divide_coupon(amount, ratios)
    except ValueError as e:
        assert str(e) == "negative amount"