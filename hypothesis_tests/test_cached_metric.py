import math
from hypothesis import given, assume, strategies as st

def cached_metric(cache, key, now):
    item = cache.get(key)
    if item is None:
        return None
    payload, ttl = item

    if now > ttl:
        return None
    return payload

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_cached_metric_early_return(cache, key, now):
    assume(cache.get(key) is None)
    assert cached_metric(cache, key, now) is None

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_cached_metric_api_call(cache, key, now):
    assert cached_metric(cache, key, now) is not None

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_cached_metric_branch_condition(cache, key, now):
    assume(cache.get(key) is not None)
    payload, ttl = cache.get(key)
    assume(now > ttl)
    assert cached_metric(cache, key, now) is None