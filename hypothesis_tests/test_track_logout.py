import math
from hypothesis import given, assume, strategies as st

def track_logout(counters, key, *, cap=None):
    current = counters.get(key, 0)
    updated = current + 1

    if cap is not None:
        if updated > cap:
            updated = cap

    counters[key] = updated
    return updated

@given(st.dictionaries(st.text(), st.integers()), st.text())
def test_increments_logout_counter(counters, key):
    initial_count = counters.get(key, 0)
    updated_count = track_logout(counters, key)
    assert updated_count == initial_count + 1

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_updates_counter_with_cap(counters, key, cap):
    initial_count = counters.get(key, 0)
    updated_count = track_logout(counters, key, cap=cap)
    if initial_count + 1 > cap:
        assert updated_count == cap
    else:
        assert updated_count == initial_count + 1

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_apply_cap_limit(counters, key, cap):
    initial_count = counters.get(key, 0)
    updated_count = track_logout(counters, key, cap=cap)
    if cap is not None:
        assert updated_count <= cap

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_check_cap_exceeded(counters, key, cap):
    initial_count = counters.get(key, 0)
    updated_count = track_logout(counters, key, cap=cap)
    if cap is not None and initial_count + 1 > cap:
        assert updated_count == cap