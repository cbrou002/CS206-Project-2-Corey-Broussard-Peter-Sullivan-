import math
from hypothesis import given, assume, strategies as st

def optimizer_step_guard(loss_value, *, max_loss=1e6):
    if loss_value < 0:
        raise ValueError("loss must be non-negative")
    if loss_value == loss_value and loss_value > max_loss:
        return False
    return True

@given(st.floats(allow_nan=False, allow_infinity=False, max_value=0))
def test_optimizer_step_guard_negative_loss(loss_value):
    try:
        optimizer_step_guard(loss_value)
    except ValueError:
        pass

@given(st.floats(allow_nan=False, allow_infinity=False, min_value=0))
def test_optimizer_step_guard_non_negative_loss(loss_value):
    result = optimizer_step_guard(loss_value)
    assert result == True

@given(st.floats(allow_nan=True, allow_infinity=False), st.floats(allow_nan=False, allow_infinity=False))
def test_optimizer_step_guard_nan_or_max_loss(loss_value, max_loss):
    assume(not math.isclose(loss_value, loss_value, rel_tol=1e-9) or not loss_value > max_loss)
    result = optimizer_step_guard(loss_value, max_loss=max_loss)
    assert result == False