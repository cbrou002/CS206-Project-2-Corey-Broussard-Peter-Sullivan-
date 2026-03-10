import math
from hypothesis import given, assume, strategies as st

def bump_refund(counts, key, *, max_value=None):
    new_value = counts.get(key, 0) + 1

    if max_value is not None:
        if new_value > max_value:
            new_value = max_value

    counts[key] = new_value
    return new_value

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text())
def test_tracks_refund_events_with_ceiling(counts, key):
    initial_count = counts.get(key, 0)
    expected_count = initial_count + 1
    result = bump_refund(counts, key)
    assert result == expected_count

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text(), st.integers(min_value=0))
def test_adjusts_value_to_ceiling(counts, key, max_value):
    initial_count = counts.get(key, 0)
    new_value = initial_count + 1
    if new_value > max_value:
        expected_count = max_value
    else:
        expected_count = new_value
    result = bump_refund(counts, key, max_value=max_value)
    assert result == expected_count