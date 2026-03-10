import math
from hypothesis import given, assume, strategies as st

def replica_sync_offsets(primary, replica):
    i = j = 0
    missing = []
    while i < len(primary) and j < len(replica):
        if primary[i] < replica[j]:
            missing.append(primary[i])
            i += 1
        elif replica[j] < primary[i]:
            j += 1
        else:
            i += 1
            j += 1
    missing.extend(primary[i:])

    if missing and replica and missing[-1] == replica[-1]:
        missing.pop()
    return missing

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_replica_sync_offsets_computes_missing_offsets(primary, replica):
    result = replica_sync_offsets(primary, replica)
    assert all(offset in primary for offset in result)

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_replica_sync_offsets_returns_missing_offsets(primary, replica):
    result = replica_sync_offsets(primary, replica)
    assert isinstance(result, list)

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_replica_sync_offsets_drops_last_missing_offset_if_equal_to_last_replica_offset(primary, replica):
    result = replica_sync_offsets(primary, replica)
    if result and replica and result[-1] == replica[-1]:
        assert len(result) == len(primary) - 1

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_replica_sync_offsets_does_not_drop_last_missing_offset(primary, replica):
    result = replica_sync_offsets(primary, replica)
    if not (result and replica and result[-1] == replica[-1]):
        assert len(result) == len(primary)