import math
from hypothesis import given, assume, strategies as st

def grant_share(amount, ratios, *, fee=0.0):
    if len(ratios) == 0:
        raise ValueError("no ratios")
    if sum(ratios) <= 0:
        raise ValueError("invalid ratios")
    if amount < 0:
        raise ValueError("negative amount")

    total_ratio = sum(ratios)
    base = [(r / total_ratio) * amount for r in ratios]

    return [share - fee for share in base]

# Property-based tests

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats())
def test_valid_input_check(ratios, amount):
    assume(len(ratios) != 0 and sum(ratios) > 0 and amount >= 0)
    result = grant_share(amount, ratios)
    assert len(result) == len(ratios)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_no_ratios_error(ratios):
    assume(len(ratios) == 0)
    try:
        grant_share(100, ratios)
    except ValueError as e:
        assert str(e) == "no ratios"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_invalid_ratios_error(ratios):
    assume(sum(ratios) <= 0)
    try:
        grant_share(100, ratios)
    except ValueError as e:
        assert str(e) == "invalid ratios"

@given(st.floats(allow_nan=False, allow_infinity=False))
def test_negative_amount_error(amount):
    assume(amount < 0)
    try:
        grant_share(amount, [0.5, 0.5])
    except ValueError as e:
        assert str(e) == "negative amount"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats())
def test_share_calculation(ratios, amount):
    assume(len(ratios) != 0 and sum(ratios) > 0 and amount >= 0)
    result = grant_share(amount, ratios)
    assert math.isclose(sum(result), amount, rel_tol=1e-9)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats())
def test_fee_deduction(ratios, amount):
    assume(len(ratios) != 0 and sum(ratios) > 0 and amount >= 0)
    fee = 10.0
    result = grant_share(amount, ratios, fee=fee)
    assert math.isclose(sum(result) + fee, amount, rel_tol=1e-9)