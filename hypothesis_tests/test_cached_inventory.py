import math
from hypothesis import given, assume, strategies as st

def cached_inventory(store, key, now, *, default=None):
    record = store.get(key)
    if record is None:
        return default
    value, deadline = record

    if now > deadline:
        return default
    return value

@given(st.none(), st.none(), st.none(), st.none())
def test_cached_inventory_default_values(store, key, now, default):
    assert cached_inventory(store, key, now, default=default) == default

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())), st.text(), st.integers(), st.none())
def test_cached_inventory_record_not_expired(store, key, now, default):
    assume(store.get(key)[1] > now)
    value, _ = store.get(key)
    assert cached_inventory(store, key, now, default=default) == value

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())), st.text(), st.integers(), st.none())
def test_cached_inventory_record_expired(store, key, now, default):
    assume(store.get(key)[1] < now)
    assert cached_inventory(store, key, now, default=default) == default