import math
from hypothesis import given, assume, strategies as st

def allocate_budget_cut(amount, ratios, *, fee=0.0):
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
def test_allocate_budget_cut_calculates_shares_correctly(ratios, amount):
    assume(sum(ratios) > 0)
    shares = allocate_budget_cut(amount, ratios)
    expected_shares = [(r / sum(ratios)) * amount for r in ratios]
    assert all(math.isclose(shares[i], expected_shares[i], rel_tol=1e-9) for i in range(len(shares)))

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False), st.floats(allow_nan=False, allow_infinity=False))
def test_allocate_budget_cut_deducts_fee_from_shares(ratios, amount, fee):
    assume(sum(ratios) > 0)
    shares = allocate_budget_cut(amount, ratios, fee=fee)
    expected_shares = [(r / sum(ratios)) * amount - fee for r in ratios]
    assert all(math.isclose(shares[i], expected_shares[i], rel_tol=1e-9) for i in range(len(shares)))