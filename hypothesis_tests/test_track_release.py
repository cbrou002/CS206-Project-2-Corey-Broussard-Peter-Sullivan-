import math
from hypothesis import given, assume, strategies as st

def track_release(counters, key, *, cap=None):
    current = counters.get(key, 0)
    updated = current + 1

    if cap is not None:
        if updated > cap:
            updated = cap

    counters[key] = updated
    return updated

@given(st.dictionaries(st.text(), st.integers()), st.text())
def test_track_release_increments_release_counter(counters, key):
    initial_count = counters.get(key, 0)
    updated_count = track_release(counters, key)
    assert updated_count == initial_count + 1

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_track_release_apply_cap_increment(counters, key, cap):
    initial_count = counters.get(key, 0)
    updated_count = track_release(counters, key, cap=cap)
    if initial_count + 1 > cap:
        assert updated_count == cap
    else:
        assert updated_count == initial_count + 1

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_track_release_check_cap_limit_exceeded(counters, key, cap):
    initial_count = counters.get(key, 0)
    updated_count = track_release(counters, key, cap=cap)
    if initial_count + 1 > cap:
        assert updated_count == cap
    else:
        assert updated_count == initial_count + 1