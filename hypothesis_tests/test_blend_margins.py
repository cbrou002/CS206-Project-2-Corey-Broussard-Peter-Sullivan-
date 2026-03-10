import math
from hypothesis import given, assume, strategies as st

def blend_margins(left, right):
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
def test_blend_margins_returns_value(left, right):
    assert blend_margins(left, right) == sorted(left + right)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_blend_margins_remove_last_matching_element(left, right):
    assume(len(left) > 0 and len(right) > 0)
    if left[-1] == right[-1]:
        expected_merged = sorted(left[:-1] + right[:-1])
    else:
        expected_merged = sorted(left + right)
    assert blend_margins(left, right) == expected_merged

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_blend_margins_control_flow_branches(left, right):
    assume(len(left) > 0 and len(right) > 0)
    merged = blend_margins(left, right)
    for i in range(len(merged) - 1):
        if left[i] < right[i]:
            assert merged[i] == left[i]
        elif right[i] < left[i]:
            assert merged[i] == right[i]
        else:
            assert merged[i] == left[i]
            assert merged[i + 1] == right[i]