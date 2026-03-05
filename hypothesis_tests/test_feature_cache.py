import math
from hypothesis import given, assume, strategies as st

def feature_cache(cache, key, now):
    item = cache.get(key)
    if item is None:
        return None
    payload, ttl = item

    if now > ttl:
        return None
    return payload

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())))
def test_feature_cache_calls_api(cache):
    assume(len(cache) > 0)
    key = list(cache.keys())[0]
    now = 10
    assert feature_cache(cache, key, now) is not None

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())))
def test_feature_cache_early_return(cache):
    assume(len(cache) > 0)
    key = list(cache.keys())[0]
    now = 5
    assert feature_cache(cache, key, now) is None