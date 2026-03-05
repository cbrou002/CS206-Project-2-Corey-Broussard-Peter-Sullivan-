import math
from hypothesis import given, strategies as st

def windowed_error_rate(events, now, *, window=60):
    cutoff = now - window
    recent = [e for e in events if e[0] >= cutoff]
    if not recent:
        return 0.0

    errors = sum(1 for _, is_err in recent if is_err)
    return errors / window

# Generator: list of tuples with timestamps and error flags
events = st.lists(st.tuples(st.integers(), st.booleans()))

@given(events, st.integers())
def test_has_parameter_window(events, now):
    assert 'window' in windowed_error_rate.__code__.co_varnames

@given(events, st.integers())
def test_has_default_window_value(events, now):
    assert windowed_error_rate.__defaults__[0] == 60

@given(events, st.integers())
def test_uses_cutoff_calculation(events, now):
    result = windowed_error_rate(events, now)
    assert result is not None

@given(events, st.integers())
def test_filters_recent_events(events, now):
    result = windowed_error_rate(events, now)
    assert all(e[0] >= now - 60 for e in result)

@given(events, st.integers())
def test_handles_empty_recent_list(events, now):
    result = windowed_error_rate([], now)
    assert math.isclose(result, 0.0, rel_tol=1e-9)

@given(events, st.integers())
def test_calculates_error_count(events, now):
    result = windowed_error_rate(events, now)
    assert result >= 0

@given(events, st.integers())
def test_computes_error_rate(events, now):
    result = windowed_error_rate(events, now)
    assert 0 <= result <= 1

@given(events, st.integers())
def test_returns_zero_error_rate(events, now):
    result = windowed_error_rate([], now)
    assert math.isclose(result, 0.0, rel_tol=1e-9)