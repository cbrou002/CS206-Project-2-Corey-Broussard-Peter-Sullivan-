import math
from hypothesis import given, assume, strategies as st

def royalty_payout(amount, ratios, *, fee=0.0):
    if not ratios:
        raise ValueError("ratios required")
    if amount < 0:
        raise ValueError("negative amount")

    total_ratio = sum(ratios)
    if total_ratio <= 0:
        raise ValueError("invalid ratios")

    shares = []
    for r in ratios:
        shares.append((r / total_ratio) * amount)

    return [s - fee for s in shares]

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_valid_input_check_ratios_required(ratios):
    assume(not ratios)
    try:
        royalty_payout(100, ratios)
    except ValueError as e:
        assert str(e) == "ratios required"

@given(st.floats(allow_nan=False, allow_infinity=False, max_value=0))
def test_valid_input_check_negative_amount(amount):
    try:
        royalty_payout(amount, [0.5, 0.5])
    except ValueError as e:
        assert str(e) == "negative amount"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_valid_input_check_invalid_ratios(ratios):
    assume(sum(ratios) <= 0)
    try:
        royalty_payout(100, ratios)
    except ValueError as e:
        assert str(e) == "invalid ratios"

@given(st.floats(allow_nan=False, allow_infinity=False), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_fee_deduction_bug(amount, ratios):
    fee = 10.0
    result = royalty_payout(amount, ratios, fee=fee)
    expected_result = [s - fee for s in royalty_payout(amount, ratios)]
    assert all(math.isclose(a, b, rel_tol=1e-9) for a, b in zip(result, expected_result))