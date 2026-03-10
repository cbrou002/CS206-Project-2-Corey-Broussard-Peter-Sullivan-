import math
from hypothesis import given, assume, strategies as st

def cache_entry_ttl(entries, key, now):
    if key not in entries:
        return None
    value, expires = entries[key]

    if now > expires:
        return None
    return value

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_cache_entry_ttl_key_not_in_entries(entries, key, now):
    assume(key not in entries)
    assert cache_entry_ttl(entries, key, now) == None

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_cache_entry_ttl_now_greater_than_expires(entries, key, now):
    assume(key in entries)
    value, expires = entries[key]
    assume(now > expires)
    assert cache_entry_ttl(entries, key, now) == None