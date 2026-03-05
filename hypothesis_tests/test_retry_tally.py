import math
from hypothesis import given, assume, strategies as st

def retry_tally(counters, key, *, cap=None):
    counters.setdefault(key, 0)
    counters[key] += 1

    if cap is not None and counters[key] > cap:
        counters[key] = cap

    return counters[key]

# Property: bump_retry_metric_with_hard_limit
@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_retry_tally_bump_retry_metric_with_hard_limit(counters, key, cap):
    assume(cap is not None)
    initial_value = counters.get(key, 0)
    expected_value = min(initial_value + 1, cap)
    
    assert retry_tally(counters, key, cap=cap) == expected_value

# Property: clamp_retry_metric_at_cap
@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_retry_tally_clamp_retry_metric_at_cap(counters, key, cap):
    assume(cap is not None)
    counters[key] = cap - 1
    expected_value = cap
    
    assert retry_tally(counters, key, cap=cap) == expected_value

# Property: no_clamp_needed
@given(st.dictionaries(st.text(), st.integers()), st.text(), st.none() | st.integers())
def test_retry_tally_no_clamp_needed(counters, key, cap):
    assume(cap is None or counters.get(key, 0) <= cap)
    initial_value = counters.get(key, 0)
    expected_value = initial_value + 1 if cap is None or initial_value < cap else initial_value
    
    assert retry_tally(counters, key, cap=cap) == expected_value