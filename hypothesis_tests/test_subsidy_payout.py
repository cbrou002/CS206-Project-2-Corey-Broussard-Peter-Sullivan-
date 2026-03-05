import math
from hypothesis import given, assume, strategies as st

def subsidy_payout(amount, ratios, *, fee=0.0):
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
def test_subsidy_payout_valid_input_check_ratios_required(ratios):
    assume(not ratios)
    try:
        subsidy_payout(100, ratios)
    except ValueError as e:
        assert str(e) == "ratios required"

@given(st.floats(allow_nan=False, allow_infinity=False, max_value=0))
def test_subsidy_payout_valid_input_check_negative_amount(amount):
    try:
        subsidy_payout(amount, [0.5, 0.5])
    except ValueError as e:
        assert str(e) == "negative amount"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_subsidy_payout_valid_input_check_invalid_ratios(ratios):
    assume(sum(ratios) <= 0)
    try:
        subsidy_payout(100, ratios)
    except ValueError as e:
        assert str(e) == "invalid ratios"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_subsidy_payout_calculation(ratios, amount):
    assume(sum(ratios) > 0)
    shares = subsidy_payout(amount, ratios)
    expected_shares = [(r / sum(ratios)) * amount for r in ratios]
    assert all(math.isclose(shares[i], expected_shares[i], rel_tol=1e-9) for i in range(len(shares)))

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_subsidy_payout_fee_deduction(ratios, amount):
    assume(sum(ratios) > 0)
    fee = 10.0
    shares = subsidy_payout(amount, ratios, fee=fee)
    expected_shares = [(r / sum(ratios)) * amount - fee for r in ratios]
    assert all(math.isclose(shares[i], expected_shares[i], rel_tol=1e-9) for i in range(len(shares)))