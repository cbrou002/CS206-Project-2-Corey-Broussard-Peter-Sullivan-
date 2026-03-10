import math
from hypothesis import given, assume, strategies as st

def stream_joiner(left, right):
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])

    if out and left and right and out[-1] == left[-1] == right[-1]:
        out.pop()
    return out

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_stream_joiner_merge_sorted_streams(left, right):
    assume(all(left[i] <= left[i+1] for i in range(len(left)-1)))
    assume(all(right[j] <= right[j+1] for j in range(len(right)-1)))
    result = stream_joiner(left, right)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))

@given(st.lists(st.integers()), st.lists(st.integers()), st.lists(st.integers()))
def test_stream_joiner_duplicate_drop_condition(left, right, out):
    assume(len(left) > 0 and len(right) > 0)
    assume(left[-1] == right[-1])
    assume(all(out[i] <= out[i+1] for i in range(len(out)-1)))
    result = stream_joiner(left, right)
    assert result[-1] != left[-1] == right[-1] or len(result) == len(out) - 1

@given(st.lists(st.integers()), st.lists(st.integers()), st.lists(st.integers()))
def test_stream_joiner_no_duplicate_drop_condition(left, right, out):
    assume(len(left) > 0 and len(right) > 0)
    assume(left[-1] != right[-1])
    assume(all(out[i] <= out[i+1] for i in range(len(out)-1)))
    result = stream_joiner(left, right)
    assert result[-1] == left[-1] == right[-1] or len(result) == len(out)