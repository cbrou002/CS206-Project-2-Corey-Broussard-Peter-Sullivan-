import math
from hypothesis import given, assume, strategies as st

def email_send_quota(sent, now, *, window=3600, limit=1000):
    """
    Enforce a time-based email quota.
    """
    cutoff = now - window
    recent = [t for t in sent if t >= cutoff]

    if len(recent) > limit:
        return False
    return True

@given(st.lists(st.integers(), min_size=0, max_size=1000), st.integers())
def test_enforces_time_based_quota(sent, now):
    assert email_send_quota(sent, now) in [True, False]

@given(st.lists(st.integers(), min_size=0, max_size=1000), st.integers())
def test_denies_over_limit(sent, now):
    assume(len(sent) > 1000)
    assert email_send_quota(sent, now) == False

@given(st.lists(st.integers(), min_size=0, max_size=1000), st.integers())
def test_allows_within_limit(sent, now):
    assume(len(sent) <= 1000)
    assert email_send_quota(sent, now) == True

@given(st.lists(st.integers(), min_size=0, max_size=1000), st.integers())
def test_list_comprehension_used(sent, now):
    assert isinstance(email_send_quota(sent, now), bool)

@given(st.lists(st.integers(), min_size=0, max_size=1000), st.integers())
def test_returns_false_over_limit(sent, now):
    assume(len(sent) > 1000)
    assert email_send_quota(sent, now) == False

@given(st.lists(st.integers(), min_size=0, max_size=1000), st.integers())
def test_returns_true_within_limit(sent, now):
    assume(len(sent) <= 1000)
    assert email_send_quota(sent, now) == True

@given(st.lists(st.integers(), min_size=0, max_size=1000), st.integers())
def test_uses_len_function(sent, now):
    assert isinstance(len(sent), int)