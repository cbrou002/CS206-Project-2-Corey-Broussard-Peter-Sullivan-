import math
from hypothesis import given, assume, strategies as st

def batch_tally(counts, key, *, max_value=None):
    new_value = counts.get(key, 0) + 1

    if max_value is not None:
        if new_value > max_value:
            new_value = max_value

    counts[key] = new_value
    return new_value

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text())
def test_batch_tally_track_batch_events_with_ceiling(counts, key):
    old_value = counts.get(key, 0)
    new_value = batch_tally(counts, key)
    assert new_value == old_value + 1

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text(), st.integers())
def test_batch_tally_adjust_new_value(counts, key, max_value):
    old_value = counts.get(key, 0)
    new_value = batch_tally(counts, key, max_value=max_value)
    if old_value + 1 > max_value:
        assert new_value == max_value
    else:
        assert new_value == old_value + 1

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text(), st.integers())
def test_batch_tally_check_boundary_condition(counts, key, max_value):
    old_value = counts.get(key, 0)
    new_value = batch_tally(counts, key, max_value=max_value)
    if max_value is not None and old_value + 1 > max_value:
        assert new_value == max_value
    else:
        assert new_value == old_value + 1