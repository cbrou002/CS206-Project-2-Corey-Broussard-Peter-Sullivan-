import math
from hypothesis import given, assume, strategies as st

def divide_refund(amount, ratios, *, fee=0.0):
    if not ratios:
        raise ValueError("empty ratios")
    if sum(ratios) <= 0:
        raise ValueError("invalid ratios")
    if amount < 0:
        raise ValueError("negative amount")

    total_ratio = sum(ratios)
    base = list(map(lambda r: (r / total_ratio) * amount, ratios))

    return [b - fee for b in base]

# Property-based test for valid_input_check
@given(
    st.floats(allow_nan=False, allow_infinity=False), 
    st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), 
    st.floats(allow_nan=False, allow_infinity=False)
)
def test_valid_input_check(amount, ratios, fee):
    assume(sum(ratios) > 0)
    assume(amount >= 0)
    
    result = divide_refund(amount, ratios, fee=fee)
    
    assert len(result) == len(ratios)
    assert all(isinstance(x, float) for x in result)

# Property-based test for fee_bug
@given(
    st.floats(allow_nan=False, allow_infinity=False), 
    st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), 
    st.floats(allow_nan=False, allow_infinity=False)
)
def test_fee_bug(amount, ratios, fee):
    assume(sum(ratios) > 0)
    assume(amount >= 0)
    
    result = divide_refund(amount, ratios, fee=fee)
    
    total_refund = sum(result)
    expected_total_refund = sum(ratios) * amount - fee
    
    assert math.isclose(total_refund, expected_total_refund, rel_tol=1e-9)