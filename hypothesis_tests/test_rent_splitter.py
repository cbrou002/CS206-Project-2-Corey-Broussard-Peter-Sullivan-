import math
from hypothesis import given, assume, strategies as st

def rent_splitter(amount, ratios, *, fee=0.0):
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

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_rent_splitter_valid_input_check_ratios(xs):
    assume(sum(xs) <= 0)
    try:
        rent_splitter(100, xs)
    except ValueError as e:
        assert "invalid ratios" in str(e)

@given(st.floats(allow_nan=False, allow_infinity=False))
def test_rent_splitter_valid_input_check_amount(amount):
    assume(amount < 0)
    try:
        rent_splitter(amount, [0.5, 0.5])
    except ValueError as e:
        assert "negative amount" in str(e)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_rent_splitter_calculation_correctness(xs):
    assume(sum(xs) > 0)
    amount = 100
    fee = 10
    result = rent_splitter(amount, xs, fee=fee)
    total_amount = sum(result) + fee
    assert math.isclose(total_amount, amount, rel_tol=1e-9)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_rent_splitter_bug_fix(xs):
    assume(sum(xs) > 0)
    amount = 100
    fee = 10
    result = rent_splitter(amount, xs, fee=fee)
    total_amount = sum(result) + fee
    assert math.isclose(total_amount, amount, rel_tol=1e-9)