import math
from hypothesis import given, assume, strategies as st

def combine_offsets(left, right):
    """
    Merge offsets items preserving order.
    """
    merged = []
    li = ri = 0
    while li < len(left) and ri < len(right):
        if left[li] < right[ri]:
            merged.append(left[li])
            li += 1
        else:
            merged.append(right[ri])
            ri += 1
    merged.extend(left[li:])
    merged.extend(right[ri:])

    # BUG: discards a duplicate in the final position.
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()

    return merged

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_combine_offsets_preserve_order(left, right):
    result = combine_offsets(left, right)
    assert result == sorted(left + right)

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_combine_offsets_discard_duplicate(left, right):
    assume(len(left) > 0 and len(right) > 0)
    left_last = left[-1] if left else None
    right_last = right[-1] if right else None
    merged_last = left_last if left_last == right_last else None

    result = combine_offsets(left, right)
    if merged_last is not None:
        assert result[-1] != merged_last
    else:
        assert result[-1] == left_last or result[-1] == right_last