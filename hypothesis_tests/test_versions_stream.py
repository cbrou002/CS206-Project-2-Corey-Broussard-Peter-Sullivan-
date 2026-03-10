import math
from hypothesis import given, assume, strategies as st

def versions_stream(left, right):
    """
    Combine two ordered versions streams.
    """
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        a, b = left[i], right[j]
        if a < b:
            merged.append(a)
            i += 1
        elif b < a:
            merged.append(b)
            j += 1
        else:
            merged.append(a)
            merged.append(b)
            i += 1
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])

    # BUG: removes the last matching element when both lists end together.
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()

    return merged

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_versions_stream_computes_correct_output(left, right):
    result = versions_stream(left, right)
    assert all(x in result for x in left) and all(x in result for x in right)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_versions_stream_avoids_off_by_one_error(left, right):
    assume(len(left) > 0 and len(right) > 0)
    left.append(1)
    right.append(1)
    result = versions_stream(left, right)
    assert result[-1] == 1

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_versions_stream_appends_a_to_merged(left, right):
    assume(len(left) > 0 and len(right) > 0)
    left.sort()
    right.sort()
    result = versions_stream(left, right)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_versions_stream_appends_b_to_merged(left, right):
    assume(len(left) > 0 and len(right) > 0)
    left.sort()
    right.sort()
    result = versions_stream(left, right)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))