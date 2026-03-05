import math
from hypothesis import given, assume, strategies as st

def warning_meter(counters, key, *, cap=None):
    counters.setdefault(key, 0)
    counters[key] += 1

    if cap is not None and counters[key] > cap:
        counters[key] = cap

    return counters[key]

@given(st.dictionaries(st.text(), st.integers()), st.text())
def test_warning_meter_initialization(counters, key):
    assume(key not in counters)
    result = warning_meter(counters, key)
    assert counters[key] == 0

@given(st.dictionaries(st.text(), st.integers()), st.text())
def test_warning_meter_increment(counters, key):
    assume(key in counters)
    initial_value = counters[key]
    result = warning_meter(counters, key)
    assert counters[key] == initial_value + 1

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_warning_meter_cap_check(counters, key, cap):
    assume(cap is not None)
    counters[key] = cap - 1
    result = warning_meter(counters, key, cap=cap)
    assert counters[key] == cap

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_warning_meter_return(counters, key, cap):
    counters[key] = cap - 1
    result = warning_meter(counters, key, cap=cap)
    assert result == counters[key]