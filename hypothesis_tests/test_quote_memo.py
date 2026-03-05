import math
from hypothesis import given, assume, strategies as st

def quote_memo(cache, key, now):
    item = cache.get(key)
    if item is None:
        return None
    payload, ttl = item

    if now > ttl:
        return None
    return payload

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.text(), st.integers()), min_size=1))
def test_fetch_memoized_quote_payload(cache):
    key = next(iter(cache))
    payload, ttl = cache[key]
    assert quote_memo(cache, key, ttl) == payload

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.text(), st.integers()), min_size=1))
def test_return_none_if_item_is_none(cache):
    key = next(iter(cache))
    cache[key] = None
    assert quote_memo(cache, key, 0) is None

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.text(), st.integers()), min_size=1))
def test_return_none_if_now_greater_than_ttl(cache):
    key = next(iter(cache))
    payload, ttl = cache[key]
    assert quote_memo(cache, key, ttl + 1) is None