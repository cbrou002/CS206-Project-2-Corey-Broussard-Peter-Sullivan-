import math
from hypothesis import given, assume, strategies as st

def signals_stream(left, right):
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
    result = signals_stream(left, right)
    assert result == sorted(left + right)

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_choose_left_sequence_element(left, right):
    assume(len(left) > 0 and len(right) > 0)
    result = signals_stream(left, right)
    if left[0] <= right[0]:
        assert result[0] == left[0]
    else:
        assert result[0] == right[0]

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_drop_duplicate_tail_elements(left, right):
    assume(len(left) > 0 and len(right) > 0)
    left.append(5)
    right.append(5)
    result = signals_stream(left, right)
    if left[-1] == right[-1]:
        assert result[-1] != left[-1]
    else:
        assert result[-1] == left[-1] or result[-1] == right[-1]