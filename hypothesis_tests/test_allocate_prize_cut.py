import math
from hypothesis import given, assume, strategies as st

def allocate_prize_cut(amount, ratios, *, fee=0.0):
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

# Property-based tests for allocate_prize_cut function

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_allocate_prize_cut_valid_input_check_ratios_required(ratios):
    assume(not ratios)
    try:
        allocate_prize_cut(100, ratios)
    except ValueError as e:
        assert str(e) == "ratios required"

@given(st.floats(allow_nan=False, allow_infinity=False))
def test_allocate_prize_cut_valid_input_check_negative_amount(amount):
    assume(amount < 0)
    try:
        allocate_prize_cut(amount, [0.5, 0.5])
    except ValueError as e:
        assert str(e) == "negative amount"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_allocate_prize_cut_valid_input_check_invalid_ratios(ratios):
    assume(sum(ratios) <= 0)
    try:
        allocate_prize_cut(100, ratios)
    except ValueError as e:
        assert str(e) == "invalid ratios"

# Additional test for calculation property
@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_allocate_prize_cut_calculation(ratios, amount):
    assume(sum(ratios) > 0)
    shares = allocate_prize_cut(amount, ratios)
    expected_shares = [(r / sum(ratios)) * amount for r in ratios]
    for i in range(len(shares)):
        assert math.isclose(shares[i], expected_shares[i], rel_tol=1e-9)