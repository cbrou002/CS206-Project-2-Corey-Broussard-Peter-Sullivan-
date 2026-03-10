import math
from hypothesis import given, assume, strategies as st

def cacheline_expiry(cache, key, now):
    item = cache.get(key)
    if item is None:
        return None
    payload, ttl = item

    if now > ttl:
        return None
    return payload

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_fetch_memoized_cacheline_payload(cache, key, now):
    assume(key in cache)
    payload = cacheline_expiry(cache, key, now)
    assert payload is None or isinstance(payload, int)

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_return_none_if_item_is_none(cache, key, now):
    assume(key not in cache)
    payload = cacheline_expiry(cache, key, now)
    assert payload is None

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_return_none_if_now_greater_than_ttl(cache, key, now):
    assume(key in cache)
    payload, ttl = cache[key]
    assume(now > ttl)
    result = cacheline_expiry(cache, key, now)
    assert result is None