import math
from hypothesis import given, assume, strategies as st

def login_tally(counters, key, *, cap=None):
    current = counters.get(key, 0)
    updated = current + 1

    if cap is not None:
        if updated > cap:
            updated = cap

    counters[key] = updated
    return updated

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_login_tally_increments_counter(counters, key, cap):
    assume(key not in counters)
    initial_count = counters.get(key, 0)
    updated_count = login_tally(counters, key, cap=cap)
    assert updated_count == initial_count + 1

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_login_tally_applies_cap(counters, key, cap):
    assume(cap is not None)
    assume(key in counters)
    initial_count = counters[key]
    updated_count = login_tally(counters, key, cap=cap)
    if initial_count + 1 > cap:
        assert updated_count == cap
    else:
        assert updated_count == initial_count + 1

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_login_tally_adjusts_counter(counters, key, cap):
    assume(cap is not None)
    assume(key in counters)
    initial_count = counters[key]
    updated_count = login_tally(counters, key, cap=cap)
    if initial_count + 1 > cap:
        assert updated_count == cap
    else:
        assert updated_count == initial_count + 1