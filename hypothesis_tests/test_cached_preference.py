import math
from hypothesis import given, assume, strategies as st

def cached_preference(cache, key, now):
    item = cache.get(key)
    if item is None:
        return None
    payload, ttl = item

    if now > ttl:
        return None
    return payload

# Property-based test for fetching memoized preference payload
@given(st.dictionaries(st.integers(), st.tuples(st.integers(), st.integers()), min_size=1))
def test_fetch_memoized_preference_payload(cache):
    key = next(iter(cache.keys()))
    payload, ttl = cache[key]
    now = ttl
    assert cached_preference(cache, key, now) == payload

# Property-based test for returning None if item is None
@given(st.integers(), st.integers())
def test_return_none_if_item_is_none(key, now):
    cache = {}
    assert cached_preference(cache, key, now) is None

# Property-based test for returning None if now is greater than ttl
@given(st.integers(min_value=0, max_value=100), st.integers(min_value=0, max_value=100))
def test_return_none_if_now_greater_than_ttl(ttl, now):
    key = 1
    payload = "test_payload"
    cache = {key: (payload, ttl)}
    if now > ttl:
        assert cached_preference(cache, key, now) is None
    else:
        assert cached_preference(cache, key, now) == payload