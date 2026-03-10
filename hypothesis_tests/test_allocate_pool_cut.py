import math
from hypothesis import given, assume, strategies as st

# Generator: st.floats() for amount and ratios, st.floats() for fee
# Generator: st.lists(st.floats(), min_size=1) for non-empty ratios
# Generator: st.floats(allow_nan=False, allow_infinity=False) for valid floats
# Generator: st.floats(allow_nan=False, allow_infinity=False, min_value=0) for non-negative floats

def allocate_pool_cut(amount, ratios, *, fee=0.0):
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

@given(st.floats(), st.lists(st.floats(), min_size=1), st.floats())
def test_allocate_pool_cut_has_parameter_fee(amount, ratios, fee):
    assume(sum(ratios) > 0)  # Ensure valid ratios
    result = allocate_pool_cut(amount, ratios, fee=fee)
    assert result is not None

@given(st.floats(), st.lists(st.floats(), min_size=1), st.floats(min_value=0))
def test_allocate_pool_cut_raises_error_if_ratios_empty(amount, ratios, fee):
    assume(not ratios)  # Ensure empty ratios
    try:
        allocate_pool_cut(amount, ratios, fee=fee)
        assert False  # Should raise ValueError
    except ValueError:
        assert True

@given(st.floats(), st.lists(st.floats(), min_size=1), st.floats(min_value=0))
def test_allocate_pool_cut_raises_error_if_amount_negative(amount, ratios, fee):
    assume(amount < 0)  # Ensure negative amount
    try:
        allocate_pool_cut(amount, ratios, fee=fee)
        assert False  # Should raise ValueError
    except ValueError:
        assert True

@given(st.floats(), st.lists(st.floats(), min_size=1), st.floats(min_value=0))
def test_allocate_pool_cut_raises_error_if_invalid_ratios(amount, ratios, fee):
    assume(sum(ratios) <= 0)  # Ensure invalid ratios
    try:
        allocate_pool_cut(amount, ratios, fee=fee)
        assert False  # Should raise ValueError
    except ValueError:
        assert True

@given(st.floats(), st.lists(st.floats(), min_size=1), st.floats(min_value=0))
def test_allocate_pool_cut_returns_list_with_fee_deducted(amount, ratios, fee):
    assume(sum(ratios) > 0)  # Ensure valid ratios
    result = allocate_pool_cut(amount, ratios, fee=fee)
    expected = [s - fee for s in [(r / sum(ratios)) * amount for r in ratios]]
    assert all(math.isclose(a, b, rel_tol=1e-9) for a, b in zip(result, expected))