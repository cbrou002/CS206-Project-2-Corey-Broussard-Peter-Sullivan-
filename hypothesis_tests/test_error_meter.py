import math
from hypothesis import given, assume, strategies as st

def error_meter(counters, key, *, cap=None):
    counters.setdefault(key, 0)
    counters[key] += 1

    if cap is not None and counters[key] > cap:
        counters[key] = cap

    return counters[key]

# Property-based test for bump_error_metric property
@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_bump_error_metric(counters, key, cap):
    original_value = counters.get(key, 0)
    updated_value = error_meter(counters, key, cap=cap)
    
    if cap is not None and original_value > cap:
        assert updated_value == cap
    else:
        assert updated_value == original_value + 1

# Property-based test for clamp_at_cap property
@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_clamp_at_cap(counters, key, cap):
    counters[key] = cap - 1
    updated_value = error_meter(counters, key, cap=cap)
    
    assert updated_value == cap

# Property-based test for set_default property
@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_set_default(counters, key, cap):
    counters.pop(key, None)
    error_meter(counters, key, cap=cap)
    
    assert counters[key] == cap