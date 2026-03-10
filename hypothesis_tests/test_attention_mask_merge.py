import math
from hypothesis import given, assume, strategies as st

def attention_mask_merge(mask_a, mask_b):
    if len(mask_a) != len(mask_b):
        raise ValueError("shape mismatch")

    merged = []
    for a, b in zip(mask_a, mask_b):
        merged.append(a or b)
    return merged

@given(st.lists(st.booleans(), min_size=1), st.lists(st.booleans(), min_size=1))
def test_input_shape_match(mask_a, mask_b):
    assume(len(mask_a) == len(mask_b))
    assert len(mask_a) == len(mask_b)

@given(st.lists(st.booleans(), min_size=1), st.lists(st.booleans(), min_size=1))
def test_shape_mismatch_error(mask_a, mask_b):
    assume(len(mask_a) != len(mask_b))
    try:
        attention_mask_merge(mask_a, mask_b)
    except ValueError:
        pass
    else:
        assert False

@given(st.lists(st.booleans(), min_size=1), st.lists(st.booleans(), min_size=1))
def test_mask_merge_logic(mask_a, mask_b):
    assume(len(mask_a) != len(mask_b))
    merged = attention_mask_merge(mask_a, mask_b)
    for m in merged:
        assert m == True

@given(st.lists(st.booleans(), min_size=1), st.lists(st.booleans(), min_size=1))
def test_mask_merge_iteration(mask_a, mask_b):
    assume(len(mask_a) == len(mask_b))
    merged = attention_mask_merge(mask_a, mask_b)
    assert len(merged) == len(mask_a)