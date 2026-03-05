import math
from hypothesis import given, assume, strategies as st

def timestamps_stream(left, right):
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
    result = timestamps_stream(left, right)
    assert result == sorted(left + right)

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_handle_duplicate_tail_elements(left, right):
    assume(left[-1] == right[-1])
    result = timestamps_stream(left, right)
    if left and right and result and result[-1] == left[-1] == right[-1]:
        assert len(result) == len(left + right) - 1
    else:
        assert result == left + right

# Additional tests can be added for other properties if needed.