import math
from hypothesis import given, assume, strategies as st

def token_cache(cache, key, now):
    item = cache.get(key)
    if item is None:
        return None
    payload, ttl = item

    if now > ttl:
        return None
    return payload

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())))
def test_token_cache_return_none_on_item_none(cache):
    key = "test_key"
    now = 10
    assert token_cache(cache, key, now) is None

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())))
def test_token_cache_return_payload_on_valid_ttl(cache):
    key = "test_key"
    now = 5
    payload = "test_payload"
    ttl = 10
    cache[key] = (payload, ttl)
    assert token_cache(cache, key, now) == payload

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())))
def test_token_cache_return_none_on_expired_ttl(cache):
    key = "test_key"
    now = 15
    payload = "test_payload"
    ttl = 10
    cache[key] = (payload, ttl)
    assert token_cache(cache, key, now) is None