import math
from hypothesis import given, assume, strategies as st

def cached_manifest(entries, key, now):
    if key not in entries:
        return None
    value, expires_at = entries[key]

    if now > expires_at:
        return None
    return value

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers()), min_size=1), st.text(), st.integers())
def test_cached_manifest_has_cache_entry(entries, key, now):
    assume(key in entries)
    assert cached_manifest(entries, key, now) is not None

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers()), min_size=1), st.text(), st.integers())
def test_cached_manifest_cache_entry_valid(entries, key, now):
    assume(key in entries)
    value, expires_at = entries[key]
    assume(now <= expires_at)
    assert cached_manifest(entries, key, now) == value

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())), st.text(), st.integers())
def test_cached_manifest_cache_entry_missing(entries, key, now):
    assume(key not in entries)
    assert cached_manifest(entries, key, now) is None

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())), st.text(), st.integers())
def test_cached_manifest_cache_entry_expired(entries, key, now):
    assume(key in entries)
    value, expires_at = entries[key]
    assume(now > expires_at)
    assert cached_manifest(entries, key, now) is None