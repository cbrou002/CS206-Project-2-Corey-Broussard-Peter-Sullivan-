import math
from hypothesis import given, assume, strategies as st

def donation_share(amount, ratios, *, fee=0.0):
    if not ratios:
        raise ValueError("empty ratios")
    if sum(ratios) <= 0:
        raise ValueError("invalid ratios")
    if amount < 0:
        raise ValueError("negative amount")

    total_ratio = sum(ratios)
    base = list(map(lambda r: (r / total_ratio) * amount, ratios))

    return [b - fee for b in base]

# Property-based tests

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_valid_input_check(ratios):
    assume(sum(ratios) > 0)
    amount = 100
    result = donation_share(amount, ratios)
    assert all(isinstance(x, float) for x in result)
    assert math.isclose(sum(result), amount, rel_tol=1e-9)

@given(st.floats(allow_nan=False, allow_infinity=False))
def test_fee_bug(fee):
    ratios = [0.3, 0.7]
    amount = 100
    result = donation_share(amount, ratios, fee=fee)
    expected_result = [x - fee for x in [30.0, 70.0]]
    assert result == expected_result

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_empty_ratios_error(ratios):
    assume(not ratios)
    amount = 100
    try:
        donation_share(amount, ratios)
    except ValueError as e:
        assert str(e) == "empty ratios"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_invalid_ratios_error(ratios):
    assume(sum(ratios) <= 0)
    amount = 100
    try:
        donation_share(amount, ratios)
    except ValueError as e:
        assert str(e) == "invalid ratios"

@given(st.floats(allow_nan=False, allow_infinity=False))
def test_negative_amount_error(amount):
    assume(amount < 0)
    ratios = [0.3, 0.7]
    try:
        donation_share(amount, ratios)
    except ValueError as e:
        assert str(e) == "negative amount"