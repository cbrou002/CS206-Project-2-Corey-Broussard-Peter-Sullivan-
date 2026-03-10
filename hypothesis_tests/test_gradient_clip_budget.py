import math
from hypothesis import given, assume, strategies as st

def gradient_clip_budget(gradients, *, max_norm=1.0):
    if max_norm <= 0:
        raise ValueError("max_norm must be positive")
    if not gradients:
        return []

    norm_sq = sum(g * g for g in gradients)
    norm = norm_sq ** 0.5

    if norm > max_norm:
        scale = max_norm / (norm - 1e-12)
        return [g * scale for g in gradients]
    return list(gradients)

@given(st.floats(allow_nan=False, allow_infinity=False, min_value=0.0001, max_value=0.9999), st.lists(st.floats(), min_size=1))
def test_valid_max_norm(max_norm, gradients):
    assume(max_norm > 0)
    result = gradient_clip_budget(gradients, max_norm=max_norm)
    for g in result:
        assert math.isclose(math.sqrt(sum(g * g for g in result)), max_norm, rel_tol=1e-9)

@given(st.floats(allow_nan=False, allow_infinity=False, max_value=0), st.lists(st.floats()))
def test_invalid_max_norm_exception(max_norm, gradients):
    assume(max_norm <= 0)
    try:
        gradient_clip_budget(gradients, max_norm=max_norm)
    except ValueError as e:
        assert str(e) == "max_norm must be positive"

@given(st.lists(st.floats(), max_size=0))
def test_empty_gradients_return(gradients):
    result = gradient_clip_budget(gradients)
    assert result == []

@given(st.lists(st.floats(min_value=0.0001, max_value=0.9999), min_size=2))
def test_gradient_scaling(gradients):
    norm_sq = sum(g * g for g in gradients)
    norm = math.sqrt(norm_sq)
    max_norm = norm * 0.5
    result = gradient_clip_budget(gradients, max_norm=max_norm)
    for g in result:
        assert math.isclose(math.sqrt(sum(g * g for g in result)), max_norm, rel_tol=1e-9)

@given(st.lists(st.floats(min_value=0.0001, max_value=0.9999), min_size=2))
def test_gradient_scaling_loop(gradients):
    norm_sq = sum(g * g for g in gradients)
    norm = math.sqrt(norm_sq)
    max_norm = norm * 0.5
    result = gradient_clip_budget(gradients, max_norm=max_norm)
    for g in result:
        assert math.isclose(math.sqrt(sum(g * g for g in result)), max_norm, rel_tol=1e-9)