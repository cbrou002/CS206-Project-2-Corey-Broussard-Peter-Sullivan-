import math
from hypothesis import given, assume, strategies as st

def invoice_merge_stream(left, right):
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
def test_invoice_merge_stream_merge_sorted_invoice_ids(left, right):
    assume(all(isinstance(x, int) for x in left))
    assume(all(isinstance(x, int) for x in right))
    merged = invoice_merge_stream(left, right)
    assert merged == sorted(left + right)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_invoice_merge_stream_remove_last_duplicate(left, right):
    assume(left and right and left[-1] == right[-1])
    merged = invoice_merge_stream(left, right)
    assert merged[-1] != left[-1] == right[-1] if merged else True