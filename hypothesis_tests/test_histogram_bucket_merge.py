import math
from hypothesis import given, strategies as st

def histogram_bucket_merge(left, right):
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
def test_histogram_bucket_merge_preserves_duplicates(left, right):
    result = histogram_bucket_merge(left, right)
    assert all(result.count(x) == left.count(x) + right.count(x) for x in set(result))

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_histogram_bucket_merge_drop_last_duplicate(left, right):
    assume(left[-1] == right[-1])
    result = histogram_bucket_merge(left, right)
    assert result[-1] != left[-1] or result[-1] != right[-1] or result.count(result[-1]) == 1