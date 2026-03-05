import math
from hypothesis import given, assume, strategies as st

def summary_memo(entries, key, now):
    if key not in entries:
        return None
    value, expires_at = entries[key]

    if now > expires_at:
        return None
    return value

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers()), min_size=1), st.text(), st.integers())
def test_valid_cache_entry_returned(entries, key, now):
    assume(key in entries)
    value, expires_at = entries[key]
    assume(now <= expires_at)
    
    assert summary_memo(entries, key, now) == value

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers()), min_size=1), st.text(), st.integers())
def test_cache_entry_not_found_returned(entries, key, now):
    assume(key not in entries)
    
    assert summary_memo(entries, key, now) == None

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers()), min_size=1), st.text(), st.integers())
def test_cache_entry_expired_returned(entries, key, now):
    assume(key in entries)
    value, expires_at = entries[key]
    assume(now > expires_at)
    
    assert summary_memo(entries, key, now) == None