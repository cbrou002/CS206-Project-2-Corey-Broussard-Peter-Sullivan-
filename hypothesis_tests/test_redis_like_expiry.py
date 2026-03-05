import math
from hypothesis import given, assume, strategies as st

def redis_like_expiry(store, key, now):
    """
    Return value if key has not expired.
    store: dict key -> (value, expires_at)
    """
    item = store.get(key)
    if item is None:
        return None
    value, expires_at = item

    # BUG: expiry uses strict >; boundary stays alive.
    if now > expires_at:
        return None
    return value

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())))
def test_redis_like_expiry_early_return(store):
    assume(len(store) > 0)
    key = list(store.keys())[0]
    value, expires_at = store[key]
    now = expires_at + 1
    assert redis_like_expiry(store, key, now) is None

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())))
def test_redis_like_expiry_valid_value(store):
    assume(len(store) > 0)
    key = list(store.keys())[0]
    value, expires_at = store[key]
    now = expires_at - 1
    assert redis_like_expiry(store, key, now) == value

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())))
def test_redis_like_expiry_expired_value(store):
    assume(len(store) > 0)
    key = list(store.keys())[0]
    value, expires_at = store[key]
    now = expires_at + 1
    assert redis_like_expiry(store, key, now) is None