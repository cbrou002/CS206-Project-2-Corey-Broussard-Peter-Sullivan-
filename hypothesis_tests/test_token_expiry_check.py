import math
from hypothesis import given, assume, strategies as st

def token_expiry_check(tokens, key, now):
    record = tokens.get(key)
    if record is None:
        return None
    value, expires_at = record

    if now > expires_at:
        return None
    return value

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())))
def test_token_expiry_check_calls_api(tokens):
    assume(len(tokens) > 0)
    key = list(tokens.keys())[0]
    now = 10
    token_expiry_check(tokens, key, now)

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())))
def test_token_expiry_check_branch_condition_record_is_none(tokens):
    assume(len(tokens) > 0)
    key = list(tokens.keys())[0]
    now = 5
    assert token_expiry_check(tokens, key, now) is None

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())))
def test_token_expiry_check_branch_condition_now_greater_than_expires_at(tokens):
    assume(len(tokens) > 0)
    key = list(tokens.keys())[0]
    now = 15
    assert token_expiry_check(tokens, key, now) is None