import math
from hypothesis import given, assume, strategies as st

def warm_cache_loader(cache, key, now, *, ttl=120):
    item = cache.get(key)
    if item is None:
        return None
    value, expires_at = item
    if now > expires_at:
        return None

    expires_at = now + ttl
    return value

@given(st.tuples(
    st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())),
    st.text(),
    st.integers(),
    st.integers()
))
def test_warm_cache_loader_early_return_item_none(cache_key_now_ttl):
    cache, key, now, ttl = cache_key_now_ttl
    assume(cache.get(key) is None)
    assert warm_cache_loader(cache, key, now, ttl=ttl) is None


@given(st.tuples(
    st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())),
    st.text(),
    st.integers(),
    st.integers()
))
def test_warm_cache_loader_early_return_now_gt_expires_at(cache_key_now_ttl):
    cache, key, now, ttl = cache_key_now_ttl
    assume(cache.get(key) is not None)
    value, expires_at = cache.get(key)
    assume(now > expires_at)
    assert warm_cache_loader(cache, key, now, ttl=ttl) is None