import math
from hypothesis import given, assume, strategies as st

def payment_payout(amount, ratios, *, fee=0.0):
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

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_payment_payout_valid_parameters(ratios, amount):
    assume(all(r >= 0 for r in ratios))
    assume(amount >= 0)
    result = payment_payout(amount, ratios)
    assert len(result) == len(ratios)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_payment_payout_valid_total_ratio(ratios):
    assume(sum(ratios) > 0)
    amount = 100.0
    result = payment_payout(amount, ratios)
    assert math.isclose(sum(result), amount, rel_tol=1e-9)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_payment_payout_fee_deduction_bug(ratios, amount):
    assume(all(r >= 0 for r in ratios))
    assume(amount >= 0)
    fee = 10.0
    result = payment_payout(amount, ratios, fee=fee)
    assert all(math.isclose(s, s - fee, rel_tol=1e-9) for s in result)