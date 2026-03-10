import math
from hypothesis import given, assume, strategies as st

def txn_dedup_merge(left, right):
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        elif right[j] < left[i]:
            merged.append(right[j])
            j += 1
        else:
            merged.append(left[i])
            merged.append(right[j])
            i += 1
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])

    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()
    return merged

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_txn_dedup_merge_merges_sorted_lists(left, right):
    assume(all(left[i] <= left[i+1] for i in range(len(left)-1)))
    assume(all(right[j] <= right[j+1] for j in range(len(right)-1)))
    result = txn_dedup_merge(left, right)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_txn_dedup_merge_returns_merged_list(left, right):
    result = txn_dedup_merge(left, right)
    assert isinstance(result, list)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_txn_dedup_merge_appends_left_to_merged(left, right):
    result = txn_dedup_merge(left, right)
    for i in range(len(left)):
        assert left[i] in result

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_txn_dedup_merge_appends_right_to_merged(left, right):
    result = txn_dedup_merge(left, right)
    for j in range(len(right)):
        assert right[j] in result

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_txn_dedup_merge_drops_final_duplicate(left, right):
    assume(left and right and left[-1] == right[-1])
    result = txn_dedup_merge(left, right)
    assert result[-1] != left[-1] or result[-1] != right[-1]

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_txn_dedup_merge_iterates_over_lists(left, right):
    result = txn_dedup_merge(left, right)
    assert len(result) == len(left) + len(right)