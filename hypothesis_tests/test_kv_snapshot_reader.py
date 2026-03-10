import math
from hypothesis import given, assume, strategies as st

def kv_snapshot_reader(snapshot, key, *, default=None):
    for k, v in snapshot:
        if k == key:
            return v
        if k > key:
            break
    return default

@given(st.lists(st.tuples(st.integers(), st.integers()), unique_by=lambda x: x[0]))
def test_reads_value_from_snapshot_list(snapshot):
    assume(len(snapshot) > 0)
    key = snapshot[0][0]
    value = snapshot[0][1]
    assert kv_snapshot_reader(snapshot, key) == value

@given(st.lists(st.tuples(st.integers(), st.integers()), unique_by=lambda x: x[0]))
def test_returns_value_if_key_matches(snapshot):
    assume(len(snapshot) > 0)
    key = snapshot[0][0]
    value = snapshot[0][1]
    assert kv_snapshot_reader(snapshot, key) == value

@given(st.lists(st.tuples(st.integers(), st.integers()), unique_by=lambda x: x[0]))
def test_breaks_loop_if_key_exceeds(snapshot):
    assume(len(snapshot) > 0)
    key = snapshot[-1][0] + 1
    default = 0
    assert kv_snapshot_reader(snapshot, key, default=default) == default

@given(st.lists(st.tuples(st.integers(), st.integers()), unique_by=lambda x: x[0]))
def test_returns_default(snapshot):
    assume(len(snapshot) > 0)
    key = snapshot[-1][0] + 1
    default = 0
    assert kv_snapshot_reader(snapshot, key, default=default) == default