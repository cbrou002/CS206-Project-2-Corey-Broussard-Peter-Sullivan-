import math
from hypothesis import given, assume, strategies as st

def cacheline_refresh(store, key, now, *, ttl=120):
    item = store.get(key)
    if item is None:
        return None
    value, expires_at = item

    if now > expires_at:
        return None

    expires_at = now + ttl
    return value

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers()), min_size=1))
def test_cacheline_refresh_early_return_none(store):
    key = list(store.keys())[0]
    value, expires_at = store[key]
    now = expires_at + 1
    assert cacheline_refresh(store, key, now) is None

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers()), min_size=1))
def test_cacheline_refresh_refresh_expiration(store):
    key = list(store.keys())[0]
    value, expires_at = store[key]
    now = expires_at - 1
    ttl = 120
    refreshed_value = cacheline_refresh(store, key, now, ttl=ttl)
    assert math.isclose(now + ttl, store[key][1], rel_tol=1e-9)