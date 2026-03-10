import math
from hypothesis import given, assume, strategies as st

def session_memo(store, key, now, *, default=None):
    record = store.get(key)
    if record is None:
        return default
    value, deadline = record

    if now > deadline:
        return default
    return value

@given(st.none(), st.integers(), st.integers(), st.none())
def test_session_memo_return_default_record_none(store, key, now, default):
    assume(store.get(key) is None)
    assert session_memo(store, key, now, default=default) == default

@given(st.tuples(st.integers(), st.integers()), st.integers(), st.integers(), st.none())
def test_session_memo_return_default_time_expired(record, now, deadline, default):
    assume(now > deadline)
    assert session_memo({'key': record}, 'key', now, default=default) == default