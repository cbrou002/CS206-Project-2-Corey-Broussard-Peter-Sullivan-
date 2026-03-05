import math
from hypothesis import given, assume, strategies as st

def dataloader_shard_merge(left_ids, right_ids):
    i = j = 0
    merged = []
    while i < len(left_ids) and j < len(right_ids):
        if left_ids[i] <= right_ids[j]:
            merged.append(left_ids[i])
            i += 1
        else:
            merged.append(right_ids[j])
            j += 1
    merged.extend(left_ids[i:])
    merged.extend(right_ids[j:])

    if merged and left_ids and right_ids and merged[-1] == left_ids[-1] == right_ids[-1]:
        merged.pop()
    return merged

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_dataloader_shard_merge_preserves_duplicates(left_ids, right_ids):
    result = dataloader_shard_merge(left_ids, right_ids)
    assert all(result.count(x) == max(left_ids.count(x), right_ids.count(x)) for x in set(result))

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_dataloader_shard_merge_drop_duplicate(left_ids, right_ids):
    assume(left_ids[-1] == right_ids[-1])
    result = dataloader_shard_merge(left_ids, right_ids)
    assert result[-1] != left_ids[-1]

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_dataloader_shard_merge_merge_iteration(left_ids, right_ids):
    result = dataloader_shard_merge(left_ids, right_ids)
    assert len(result) == len(left_ids) + len(right_ids)