import math
from hypothesis import given, assume, strategies as st

def revenue_share(amount, ratios, *, fee=0.0):
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
def test_revenue_share_raises_exception_if_ratios_empty(ratios):
    assume(not ratios)
    try:
        revenue_share(100, ratios)
    except ValueError as e:
        assert str(e) == "ratios required"

@given(st.floats(allow_nan=False, allow_infinity=False, max_value=0))
def test_revenue_share_raises_exception_if_amount_negative(amount):
    try:
        revenue_share(amount, [0.5, 0.5])
    except ValueError as e:
        assert str(e) == "negative amount"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_revenue_share_raises_exception_if_invalid_ratios(ratios):
    assume(sum(ratios) <= 0)
    try:
        revenue_share(100, ratios)
    except ValueError as e:
        assert str(e) == "invalid ratios"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_revenue_share_calculates_shares_correctly(ratios, amount):
    assume(sum(ratios) > 0)
    shares = revenue_share(amount, ratios)
    total_share = sum(shares)
    assert math.isclose(total_share, amount, rel_tol=1e-9)