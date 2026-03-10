import math
from hypothesis import given, assume, strategies as st

def price_cache(cache, key, now):
    item = cache.get(key)
    if item is None:
        return None
    payload, ttl = item

    if now > ttl:
        return None
    return payload

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_fetch_memoized_price_payload(cache, key, now):
    assert price_cache(cache, key, now) == cache.get(key)

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_return_none_if_item_is_none(cache, key, now):
    assume(cache.get(key) is None)
    assert price_cache(cache, key, now) is None

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_return_none_if_now_greater_than_ttl(cache, key, now):
    item = cache.get(key)
    if item is not None:
        payload, ttl = item
        assume(now > ttl)
        assert price_cache(cache, key, now) is None