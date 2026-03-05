import math
from hypothesis import given, assume, strategies as st

def catalog_cache(entries, key, now):
    if key not in entries:
        return None
    value, expires_at = entries[key]

    if now > expires_at:
        return None
    return value

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_catalog_cache_key_not_in_entries(entries, key, now):
    assume(key not in entries)
    assert catalog_cache(entries, key, now) == None

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_catalog_cache_key_in_entries_expired(entries, key, now):
    assume(key in entries)
    value, expires_at = entries[key]
    assume(now > expires_at)
    assert catalog_cache(entries, key, now) == None

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_catalog_cache_key_in_entries_not_expired(entries, key, now):
    assume(key in entries)
    value, expires_at = entries[key]
    assume(now <= expires_at)
    assert catalog_cache(entries, key, now) == value