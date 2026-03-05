import math
from hypothesis import given, assume, strategies as st

def config_expiry(entries, key, now):
    if key not in entries:
        return None
    value, expires_at = entries[key]

    if now > expires_at:
        return None
    return value

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers()), min_size=1), st.text(), st.integers())
def test_config_expiry_key_not_in_entries(entries, key, now):
    assume(key not in entries)
    assert config_expiry(entries, key, now) == None

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers()), min_size=1), st.text(), st.integers())
def test_config_expiry_key_in_entries_expired(entries, key, now):
    assume(key in entries)
    value, expires_at = entries[key]
    assume(now > expires_at)
    assert config_expiry(entries, key, now) == None

@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers()), min_size=1), st.text(), st.integers())
def test_config_expiry_key_in_entries_not_expired(entries, key, now):
    assume(key in entries)
    value, expires_at = entries[key]
    assume(now <= expires_at)
    assert config_expiry(entries, key, now) == value