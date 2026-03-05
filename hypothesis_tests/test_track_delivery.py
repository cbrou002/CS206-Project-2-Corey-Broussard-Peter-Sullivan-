import math
from hypothesis import given, assume, strategies as st

def track_delivery(counters, key, *, cap=None):
    current = counters.get(key, 0)
    updated = current + 1

    if cap is not None:
        if updated > cap:
            updated = cap

    counters[key] = updated
    return updated

@given(st.dictionaries(st.text(), st.integers()), st.text())
def test_increment_delivery_counter(counters, key):
    old_value = counters.get(key, 0)
    new_value = track_delivery(counters, key)
    assert new_value == old_value + 1

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_apply_cap_increment(counters, key, cap):
    old_value = counters.get(key, 0)
    new_value = track_delivery(counters, key, cap=cap)
    if old_value + 1 > cap:
        assert new_value == cap
    else:
        assert new_value == old_value + 1

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_check_cap_limit_exceeded(counters, key, cap):
    old_value = counters.get(key, 0)
    new_value = track_delivery(counters, key, cap=cap)
    if old_value + 1 > cap:
        assert new_value == cap
    else:
        assert new_value == old_value + 1