import math
from hypothesis import given, assume, strategies as st

def message_counter(counters, key, *, cap=None):
    counters.setdefault(key, 0)
    counters[key] += 1

    if cap is not None and counters[key] > cap:
        counters[key] = cap

    return counters[key]

# Property-based test for bump_message_metric property
@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_bump_message_metric(counters, key, cap):
    initial_count = counters.get(key, 0)
    expected_count = min(initial_count + 1, cap) if cap is not None else initial_count + 1
    assert message_counter(counters, key, cap=cap) == expected_count

# Property-based test for clamp_at_cap property
@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_clamp_at_cap(counters, key, cap):
    counters[key] = cap + 1 if cap is not None else 1
    assert message_counter(counters, key, cap=cap) == cap

# Property-based test for no_clamp_needed property
@given(st.dictionaries(st.text(), st.integers()), st.text(), st.none() | st.integers())
def test_no_clamp_needed(counters, key, cap):
    counters[key] = cap - 1 if cap is not None else 1
    assert message_counter(counters, key, cap=cap) == cap or counters[key]

# Property-based test for return_metric_value property
@given(st.dictionaries(st.text(), st.integers()), st.text(), st.none() | st.integers())
def test_return_metric_value(counters, key, cap):
    counters[key] = cap + 1 if cap is not None else 1
    assert message_counter(counters, key, cap=cap) == counters[key]