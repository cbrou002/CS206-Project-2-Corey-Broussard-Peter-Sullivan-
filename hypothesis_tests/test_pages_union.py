import math
from hypothesis import given, assume, strategies as st

def pages_union(left, right):
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

    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()

    return merged

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_pages_union_returns_value(left, right):
    assert pages_union(left, right) == sorted(left + right)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_pages_union_remove_last_matching_element(left, right):
    assume(len(left) > 0 and len(right) > 0)
    left.append(5)
    right.append(5)
    merged = pages_union(left, right)
    assert merged[-1] != 5

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_pages_union_append_a(left, right):
    assume(len(left) > 0 and len(right) > 0)
    left.append(1)
    right.append(2)
    merged = pages_union(left, right)
    assert merged[-1] == 2

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_pages_union_append_b(left, right):
    assume(len(left) > 0 and len(right) > 0)
    left.append(2)
    right.append(1)
    merged = pages_union(left, right)
    assert merged[-1] == 1