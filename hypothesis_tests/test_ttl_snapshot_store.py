import math
from hypothesis import given, assume, strategies as st

def ttl_snapshot_store(entries, key, now):
    if key not in entries:
        return None
    value, expires_at = entries[key]

    if now > expires_at:
        return None
    return value

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_ttl_snapshot_store_early_return(entries, key, now):
    assume(key not in entries)
    assert ttl_snapshot_store(entries, key, now) == None

@given(st.dictionaries(keys=st.integers(), values=st.tuples(st.integers(), st.integers())), st.integers(), st.integers())
def test_ttl_snapshot_store_branch_early_return(entries, key, now):
    assume(now > entries[key][1])
    assert ttl_snapshot_store(entries, key, now) == None