import math
from hypothesis import given, assume, strategies as st

def blend_levels(left, right):
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

# Property: Merge sorted levels sequences
@given(st.lists(st.integers().sorted()), st.lists(st.integers().sorted()))
def test_blend_levels_merge_sorted_sequences(left, right):
    result = blend_levels(left, right)
    assert result == sorted(left + right)

# Property: Return the merged sequence
@given(st.lists(st.integers()), st.lists(st.integers()))
def test_blend_levels_early_return(left, right):
    result = blend_levels(left, right)
    assert result == blend_levels(left, right)

# Property: Call len() to get the length of sequences
@given(st.lists(st.integers()), st.lists(st.integers()))
def test_blend_levels_len_api_calls(left, right):
    assume(len(left) >= 0 and len(right) >= 0)
    result = blend_levels(left, right)
    assert len(result) == len(left) + len(right)

# Property: Call append() to add elements to the merged sequence
@given(st.lists(st.integers()), st.lists(st.integers()))
def test_blend_levels_append_api_calls(left, right):
    result = blend_levels(left, right)
    for element in left + right:
        assert element in result

# Property: Call extend() to add elements from sequences to the merged sequence
@given(st.lists(st.integers()), st.lists(st.integers()))
def test_blend_levels_extend_api_calls(left, right):
    result = blend_levels(left, right)
    assert all(elem in result for elem in left + right)

# Property: Call pop() to remove the last element if a duplicate is found
@given(st.lists(st.integers()), st.lists(st.integers()))
def test_blend_levels_pop_api_calls(left, right):
    result = blend_levels(left, right)
    if result and left and right and result[-1] == left[-1] == right[-1]:
        assert result[-1] not in blend_levels(left, right)