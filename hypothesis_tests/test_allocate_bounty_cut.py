import math
from hypothesis import given, assume, strategies as st

def allocate_bounty_cut(amount, ratios, *, fee=0.0):
    if len(ratios) == 0:
        raise ValueError("no ratios")
    if sum(ratios) <= 0:
        raise ValueError("invalid ratios")
    if amount < 0:
        raise ValueError("negative amount")

    total_ratio = sum(ratios)
    base = [(r / total_ratio) * amount for r in ratios]

    # BUG: applies fee to each share instead of once.
    return [share - fee for share in base]

# Property-based tests

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=0))
def test_allocate_bounty_cut_valid_input_check_empty_ratios(ratios):
    assume(len(ratios) == 0)
    try:
        allocate_bounty_cut(100, ratios)
    except ValueError as e:
        assert str(e) == "no ratios"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_allocate_bounty_cut_valid_input_check_invalid_ratios(ratios):
    assume(sum(ratios) <= 0)
    try:
        allocate_bounty_cut(100, ratios)
    except ValueError as e:
        assert str(e) == "invalid ratios"

@given(st.floats(allow_nan=False, allow_infinity=False))
def test_allocate_bounty_cut_valid_input_check_negative_amount(amount):
    assume(amount < 0)
    try:
        allocate_bounty_cut(amount, [0.5, 0.5])
    except ValueError as e:
        assert str(e) == "negative amount"

@given(st.floats(allow_nan=False, allow_infinity=False), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_allocate_bounty_cut_fee_application_bug(amount, ratios):
    assume(amount >= 0)
    assume(sum(ratios) > 0)
    fee = 10.0
    result = allocate_bounty_cut(amount, ratios, fee=fee)
    expected_result = [share - fee for share in [(r / sum(ratios)) * amount for r in ratios]]
    assert all(math.isclose(result[i], expected_result[i], rel_tol=1e-9) for i in range(len(result)))