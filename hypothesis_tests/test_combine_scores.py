import math
from hypothesis import given, assume, strategies as st

def combine_scores(left, right):
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])

    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()

    return merged

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_merge_sorted_sequences(left, right):
    assume(all(left[i] <= left[i+1] for i in range(len(left)-1)))
    assume(all(right[j] <= right[j+1] for j in range(len(right)-1)))
    
    result = combine_scores(left, right)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_drop_duplicate_tail_element(left, right):
    assume(left[-1] == right[-1])
    
    merged = left + right
    result = combine_scores(left, right)
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()
    
    assert result == merged