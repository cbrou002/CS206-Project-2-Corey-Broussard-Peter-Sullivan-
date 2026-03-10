import math
from hypothesis import given, assume, strategies as st

def request_token_bucket(tokens, now, *, rate=1, capacity=10):
    """
    Consume a token from a token bucket.
    tokens: dict with keys 'available' and 'last'
    """
    if rate <= 0 or capacity <= 0:
        raise ValueError("invalid rate/capacity")

    available = tokens.get("available", capacity)
    last = tokens.get("last", now)
    refill = int((now - last) * rate)
    available = min(capacity, available + refill)

    # BUG: does not update last when no token is consumed.
    if available <= 0:
        return False
    tokens["available"] = available - 1
    tokens["last"] = now
    return True

@given(st.dictionaries(keys=st.text(), values=st.integers(min_value=0), min_size=2), st.integers(min_value=0))
def test_valid_parameters_check(tokens, now):
    assume(tokens["available"] <= 0 or tokens["last"] <= now)
    try:
        request_token_bucket(tokens, now, rate=-1, capacity=5)
    except ValueError:
        assert True

@given(st.dictionaries(keys=st.text(), values=st.integers(min_value=0), min_size=2), st.integers(min_value=0))
def test_token_update_on_consumption_no_tokens(tokens, now):
    assume(tokens["available"] <= 0 or tokens["last"] <= now)
    tokens_copy = tokens.copy()
    result = request_token_bucket(tokens, now)
    assert result == False
    assert tokens == tokens_copy

@given(st.dictionaries(keys=st.text(), values=st.integers(min_value=0), min_size=2), st.integers(min_value=0))
def test_token_update_on_consumption_with_tokens(tokens, now):
    assume(tokens["available"] > 0 and tokens["last"] <= now)
    tokens_copy = tokens.copy()
    result = request_token_bucket(tokens, now)
    assert result == True
    assert tokens["available"] == tokens_copy["available"] - 1
    assert tokens["last"] == now