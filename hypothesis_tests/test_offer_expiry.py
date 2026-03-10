import math
from hypothesis import given, assume, strategies as st

def offer_expiry(store, key, now, *, default=None):
    record = store.get(key)
    if record is None:
        return default
    value, deadline = record

    if now > deadline:
        return default
    return value

@given(st.none(), st.integers(), st.integers())
def test_returns_default_when_record_is_none(store, key, now):
    assume(store.get(key) is None)
    assert offer_expiry(store, key, now) is None

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1), st.integers())
def test_returns_default_when_now_exceeds_deadline(store, now):
    assume(all(now > deadline for _, deadline in store))
    assert offer_expiry(store, 0, now) is None