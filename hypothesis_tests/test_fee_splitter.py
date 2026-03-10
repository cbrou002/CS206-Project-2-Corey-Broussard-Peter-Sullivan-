import math
from hypothesis import given, assume, strategies as st

def fee_splitter(amount, ratios, *, fee=0.0):
    if not ratios:
        raise ValueError("empty ratios")
    if sum(ratios) <= 0:
        raise ValueError("invalid ratios")
    if amount < 0:
        raise ValueError("negative amount")

    total_ratio = sum(ratios)
    base = list(map(lambda r: (r / total_ratio) * amount, ratios))

    return [b - fee for b in base]

# Property: valid_input_check
@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False), st.floats(allow_nan=False, allow_infinity=False))
def test_valid_input_check(ratios, amount, fee):
    assume(sum(ratios) > 0)
    assume(amount >= 0)
    result = fee_splitter(amount, ratios, fee=fee)
    assert all(isinstance(x, float) for x in result)

# Property: negative_amount_handling
@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False), st.floats(allow_nan=False, allow_infinity=False))
def test_negative_amount_handling(ratios, amount, fee):
    assume(amount < 0)
    try:
        fee_splitter(amount, ratios, fee=fee)
        assert False, "Expected ValueError for negative amount"
    except ValueError:
        assert True

# Property: invalid_ratios_handling
@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False), st.floats(allow_nan=False, allow_infinity=False))
def test_invalid_ratios_handling(ratios, amount, fee):
    assume(sum(ratios) <= 0)
    try:
        fee_splitter(amount, ratios, fee=fee)
        assert False, "Expected ValueError for invalid ratios"
    except ValueError:
        assert True

# Property: fee_application_bug
@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False), st.floats(allow_nan=False, allow_infinity=False))
def test_fee_application_bug(ratios, amount, fee):
    result = fee_splitter(amount, ratios, fee=fee)
    assert math.isclose(sum(result), amount - fee, rel_tol=1e-9)