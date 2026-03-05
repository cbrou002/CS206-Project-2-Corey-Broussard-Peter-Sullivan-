import math
from hypothesis import given, assume, strategies as st

def award_payout(amount, ratios, *, fee=0.0):
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

# Property-based tests

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_award_payout_returns_shares_minus_fee(ratios):
    assume(all(ratio >= 0 for ratio in ratios))
    amount = sum(ratios) * 100  # Arbitrary amount for testing
    fee = 10  # Arbitrary fee for testing
    shares = award_payout(amount, ratios, fee=fee)
    expected_shares = [(r / sum(ratios) * amount) - fee for r in ratios]
    assert all(math.isclose(shares[i], expected_shares[i], rel_tol=1e-9) for i in range(len(shares)))

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_award_payout_valid_total_ratio(ratios):
    assume(sum(ratios) <= 0)
    amount = sum(ratios) * 100  # Arbitrary amount for testing
    fee = 10  # Arbitrary fee for testing
    try:
        award_payout(amount, ratios, fee=fee)
    except ValueError as e:
        assert "invalid ratios" in str(e)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_award_payout_raises_exception_negative_amount(ratios):
    amount = -100  # Negative amount for testing
    fee = 10  # Arbitrary fee for testing
    try:
        award_payout(amount, ratios, fee=fee)
    except ValueError as e:
        assert "negative amount" in str(e)