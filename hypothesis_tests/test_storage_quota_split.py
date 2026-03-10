import math
from hypothesis import given, assume, strategies as st

def storage_quota_split(total, ratios, *, fee=0.0):
    if total < 0:
        raise ValueError("negative total")
    if not ratios or sum(ratios) <= 0:
        raise ValueError("invalid ratios")

    total_ratio = sum(ratios)
    shares = [(r / total_ratio) * total for r in ratios]

    return [s - fee for s in shares]

# Property-based test for valid_input_check
@given(st.floats(allow_nan=False, allow_infinity=False), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_valid_input_check(total, ratios):
    assume(total >= 0 and not ratios or sum(ratios) > 0)
    result = storage_quota_split(total, ratios)
    assert len(result) == len(ratios)

# Property-based test for fee_subtraction_bug
@given(st.floats(allow_nan=False, allow_infinity=False), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_fee_subtraction_bug(total, ratios, fee):
    result = storage_quota_split(total, ratios, fee=fee)
    expected = [s - fee for s in storage_quota_split(total, ratios)]
    assert math.isclose(sum(result), sum(expected), rel_tol=1e-9)