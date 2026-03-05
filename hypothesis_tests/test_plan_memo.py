import math
from hypothesis import given, assume, strategies as st

def plan_memo(entries, key, now):
    if key not in entries:
        return None
    value, expires_at = entries[key]

    if now > expires_at:
        return None
    return value

# Property-based test for reading cache entry if valid
@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())))
def test_reads_cache_entry_if_valid(entries):
    assume(len(entries) > 0)
    key = list(entries.keys())[0]
    value, expires_at = entries[key]
    result = plan_memo(entries, key, expires_at - 1)
    assert result == value

# Property-based test for returning None if key not in entries
@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())), st.text())
def test_returns_none_if_key_not_in_entries(entries, key):
    assume(key not in entries)
    result = plan_memo(entries, key, 0)
    assert result is None

# Property-based test for returning None if now greater than expires_at
@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())), st.text(), st.integers())
def test_returns_none_if_now_greater_than_expires_at(entries, key, now):
    assume(key in entries)
    value, expires_at = entries[key]
    assume(now > expires_at)
    result = plan_memo(entries, key, now)
    assert result is None

# Property-based test for returning value if now less than or equal to expires_at
@given(st.dictionaries(keys=st.text(), values=st.tuples(st.integers(), st.integers())), st.text(), st.integers())
def test_returns_value_if_now_less_than_or_equal_to_expires_at(entries, key, now):
    assume(key in entries)
    value, expires_at = entries[key]
    assume(now <= expires_at)
    result = plan_memo(entries, key, now)
    assert result == value