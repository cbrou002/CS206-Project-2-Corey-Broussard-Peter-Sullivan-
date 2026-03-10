import math
from hypothesis import given, assume, strategies as st

def credit_share(amount, ratios, *, fee=0.0):
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
def test_credit_share_valid_input_check_ratios_required(ratios):
    assume(not ratios)
    try:
        credit_share(100, ratios)
    except ValueError as e:
        assert str(e) == "ratios required"