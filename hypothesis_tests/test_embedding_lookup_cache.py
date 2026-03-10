import math
from hypothesis import given, assume, strategies as st

def embedding_lookup_cache(cache, key, now, *, ttl=300):
    item = cache.get(key)
    if item is None:
        return None
    value, cached_at = item

    if now > cached_at + ttl:
        return None
    return value

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_embedding_lookup_cache_returns_cached_embedding(cache, key, now):
    assume(key in cache)
    value, cached_at = cache[key]
    result = embedding_lookup_cache(cache, key, now)
    assert result == value

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_embedding_lookup_cache_returns_none_if_expired(cache, key, now):
    assume(key in cache)
    value, cached_at = cache[key]
    ttl = 300
    now = cached_at + ttl + 1
    result = embedding_lookup_cache(cache, key, now)
    assert result is None