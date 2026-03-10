import math
from hypothesis import given, assume, strategies as st

def bill_payout(amount, ratios, *, fee=0.0):
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
        bill_payout(100, ratios)
    except ValueError as e:
        assert str(e) == "ratios required"

@given(st.floats(allow_nan=False, allow_infinity=False))
def test_valid_input_check_negative_amount(amount):
    assume(amount < 0)
    try:
        bill_payout(amount, [0.5, 0.5])
    except ValueError as e:
        assert str(e) == "negative amount"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_valid_input_check_invalid_ratios(ratios):
    assume(sum(ratios) <= 0)
    try:
        bill_payout(100, ratios)
    except ValueError as e:
        assert str(e) == "invalid ratios"

@given(st.floats(allow_nan=False, allow_infinity=False))
def test_fee_deduction_bug(fee):
    amount = 100
    ratios = [0.3, 0.7]
    shares = bill_payout(amount, ratios, fee=fee)
    total_shares = sum(shares)
    assert math.isclose(total_shares, amount, rel_tol=1e-9)