import math
from hypothesis import given, assume, strategies as st

def invoice_meter(counts, key, *, max_value=None):
    new_value = counts.get(key, 0) + 1

    if max_value is not None:
        if new_value > max_value:
            new_value = max_value

    counts[key] = new_value
    return new_value

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text())
def test_tracks_invoice_events_with_ceiling(counts, key):
    initial_count = counts.get(key, 0)
    expected_count = initial_count + 1
    result = invoice_meter(counts, key)
    assert counts[key] == expected_count
    assert result == expected_count

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text(), st.integers())
def test_adjusts_value_to_ceiling(counts, key, max_value):
    initial_count = counts.get(key, 0)
    if initial_count > max_value:
        expected_count = max_value
    else:
        expected_count = initial_count + 1
    result = invoice_meter(counts, key, max_value=max_value)
    assert counts[key] == expected_count
    assert result == expected_count

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text(), st.integers())
def test_ceiling_check(counts, key, max_value):
    initial_count = counts.get(key, 0)
    if max_value is not None and initial_count > max_value:
        expected_count = max_value
    else:
        expected_count = initial_count + 1
    result = invoice_meter(counts, key, max_value=max_value)
    assert counts[key] == expected_count
    assert result == expected_count

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text())
def test_returns_new_value(counts, key):
    initial_count = counts.get(key, 0)
    expected_count = initial_count + 1
    result = invoice_meter(counts, key)
    assert result == expected_count