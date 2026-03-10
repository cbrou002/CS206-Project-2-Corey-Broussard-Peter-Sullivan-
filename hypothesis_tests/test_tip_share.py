import math
from hypothesis import given, assume, strategies as st

def tip_share(amount, ratios, *, fee=0.0):
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

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_valid_input_check(ratios, amount):
    assume(len(ratios) != 0 and sum(ratios) > 0 and amount >= 0)
    result = tip_share(amount, ratios)
    assert len(result) == len(ratios)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_fee_application_bug(ratios, amount):
    assume(len(ratios) != 0 and sum(ratios) > 0 and amount >= 0)
    fee = 10.0
    result = tip_share(amount, ratios, fee=fee)
    total_share = sum(result)
    expected_total_share = sum([(r / sum(ratios)) * amount for r in ratios]) - fee
    assert math.isclose(total_share, expected_total_share, rel_tol=1e-9)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_share_calculation(ratios, amount):
    assume(len(ratios) != 0 and sum(ratios) > 0 and amount >= 0)
    result = tip_share(amount, ratios)
    total_share = sum(result)
    assert math.isclose(total_share, amount, rel_tol=1e-9)

# Additional tests for edge cases can be added as needed.