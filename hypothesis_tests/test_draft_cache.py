import math
from hypothesis import given, assume, strategies as st

def draft_cache(entries, key, now):
    if key not in entries:
        return None
    value, expires_at = entries[key]

    if now > expires_at:
        return None
    return value

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_draft_cache_entry_not_in_entries(entries, key, now):
    assume(key not in entries)
    assert draft_cache(entries, key, now) == None

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_draft_cache_entry_expired(entries, key, now):
    assume(key in entries)
    value, expires_at = entries[key]
    assume(now > expires_at)
    assert draft_cache(entries, key, now) == None

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_draft_cache_entry_valid(entries, key, now):
    assume(key in entries)
    value, expires_at = entries[key]
    assume(now <= expires_at)
    assert draft_cache(entries, key, now) == value