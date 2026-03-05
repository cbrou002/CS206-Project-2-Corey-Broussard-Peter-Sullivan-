import math
from hypothesis import given, assume, strategies as st

def profile_expiry(entries, key, now):
    if key not in entries:
        return None
    value, expires_at = entries[key]

    if now > expires_at:
        return None
    return value

@given(st.dictionaries(st.integers(), st.tuples(st.integers(), st.integers()), min_size=1), st.integers(), st.integers())
def test_profile_expiry_has_early_return(entries, key, now):
    assume(key not in entries)
    assert profile_expiry(entries, key, now) == None

@given(st.dictionaries(st.integers(), st.tuples(st.integers(), st.integers()), min_size=1), st.integers(), st.integers())
def test_profile_expiry_branch_has_early_return(entries, key, now):
    assume(now > entries[key][1])
    assert profile_expiry(entries, key, now) == None