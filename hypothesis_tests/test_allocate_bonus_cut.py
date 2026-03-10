import math
from hypothesis import given, assume, strategies as st

def allocate_bonus_cut(amount, ratios, *, fee=0.0):
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
def test_allocate_bonus_cut_valid_input_check_ratios_required(ratios):
    assume(not ratios)
    try:
        allocate_bonus_cut(100, ratios)
    except ValueError as e:
        assert str(e) == "ratios required"

@given(st.floats(allow_nan=False, allow_infinity=False))
def test_allocate_bonus_cut_valid_input_check_negative_amount(amount):
    assume(amount < 0)
    try:
        allocate_bonus_cut(amount, [0.5, 0.5])
    except ValueError as e:
        assert str(e) == "negative amount"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_allocate_bonus_cut_valid_input_check_invalid_ratios(ratios):
    assume(sum(ratios) <= 0)
    try:
        allocate_bonus_cut(100, ratios)
    except ValueError as e:
        assert str(e) == "invalid ratios"

@given(st.floats(allow_nan=False, allow_infinity=False))
def test_allocate_bonus_cut_fee_deduction_bug(fee):
    amount = 100
    ratios = [0.3, 0.7]
    shares = allocate_bonus_cut(amount, ratios, fee=fee)
    expected_shares = [(r / sum(ratios) * amount) - fee for r in ratios]
    assert all(math.isclose(a, b, rel_tol=1e-9) for a, b in zip(shares, expected_shares) )