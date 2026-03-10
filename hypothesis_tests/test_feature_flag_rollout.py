import math
from hypothesis import given, assume, strategies as st

def feature_flag_rollout(user_id, *, percentage=0.1):
    if not (0 <= percentage <= 1):
        raise ValueError("percentage must be in [0, 1]")

    bucket = (hash(user_id) % 100) / 100.0

    # BUG: uses > instead of < so rollout is inverted.
    return bucket > percentage

@given(st.floats(min_value=0, max_value=1))
def test_valid_percentage_range(percentage):
    assume(0 <= percentage <= 1)
    try:
        feature_flag_rollout(123, percentage=percentage)
    except ValueError:
        assert False, "ValueError should not be raised for valid percentage range"

@given(st.floats().filter(lambda x: x < 0 or x > 1))
def test_percentage_check_invalid(percentage):
    assume(not 0 <= percentage <= 1)
    assert not feature_flag_rollout(123, percentage=percentage)

@given(st.floats(min_value=0, max_value=1))
def test_percentage_check_valid(percentage):
    assume(0 <= percentage <= 1)
    assert feature_flag_rollout(123, percentage=percentage) == (hash(123) % 100) / 100.0 > percentage

# Additional tests can be added for more coverage and edge cases.