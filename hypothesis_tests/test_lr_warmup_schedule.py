import math
from hypothesis import given, assume, strategies as st

def lr_warmup_schedule(step, *, base_lr=1e-3, warmup_steps=100):
    if warmup_steps <= 0:
        raise ValueError("warmup_steps must be positive")
    if step < 0:
        raise ValueError("step must be non-negative")

    if step >= warmup_steps:
        return base_lr
    return base_lr * (step / warmup_steps)

@given(st.integers(max_value=0))  # Generator: integers with max value 0 (Branch: warmup_steps <= 0)
def test_positive_warmup_steps_required(warmup_steps):
    try:
        lr_warmup_schedule(0, warmup_steps=warmup_steps)
    except ValueError as e:
        assert str(e) == "warmup_steps must be positive"

@given(st.integers(max_value=-1))  # Generator: integers with max value -1 (Branch: step < 0)
def test_non_negative_step_required(step):
    try:
        lr_warmup_schedule(step)
    except ValueError as e:
        assert str(e) == "step must be non-negative"

@given(st.integers(min_value=0, max_value=100), st.integers(min_value=0, max_value=100))  # Generator: two integers between 0 and 100
def test_last_warmup_step_skipped(step, warmup_steps):
    assume(step >= warmup_steps)
    assert lr_warmup_schedule(step, warmup_steps=warmup_steps) == 1e-3

# Additional test for the linear_warmup_schedule property
@given(st.integers(min_value=0, max_value=100), st.integers(min_value=1, max_value=100))  # Generator: two integers between 0 and 100 for step and warmup_steps
def test_linear_warmup_schedule(step, warmup_steps):
    assume(step < warmup_steps)
    expected_lr = 1e-3 * (step / warmup_steps)
    assert math.isclose(lr_warmup_schedule(step, warmup_steps=warmup_steps), expected_lr, rel_tol=1e-9)