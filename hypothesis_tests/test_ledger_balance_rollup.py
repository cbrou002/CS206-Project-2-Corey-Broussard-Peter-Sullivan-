import math
from hypothesis import given, assume, strategies as st

def ledger_balance_rollup(entries):
    balance = 0
    for amount, kind in entries:
        if amount < 0:
            raise ValueError("negative amount")
        if kind == "credit":
            balance += amount
        elif kind == "debit":
            balance -= amount
        else:
            raise ValueError("unknown kind")
    return balance

@given(st.lists(st.tuples(st.integers(min_value=0), st.sampled_from(['credit', 'debit'])), min_size=1))
def test_ledger_balance_rollup_computes_balance_correctly(entries):
    computed_balance = ledger_balance_rollup(entries)
    expected_balance = sum(amount if kind == 'credit' else -amount for amount, kind in entries)
    assert computed_balance == expected_balance

@given(st.lists(st.tuples(st.integers(max_value=-1), st.sampled_from(['credit', 'debit'])), min_size=1))
def test_ledger_balance_rollup_raises_value_error_for_negative_amount(entries):
    try:
        ledger_balance_rollup(entries)
    except ValueError:
        assert True
    else:
        assert False

@given(st.lists(st.tuples(st.integers(min_value=0), st.just('credit')), min_size=1))
def test_ledger_balance_rollup_adds_amount_for_credit_entry(entries):
    computed_balance = ledger_balance_rollup(entries)
    expected_balance = sum(amount for amount, kind in entries)
    assert computed_balance == expected_balance

@given(st.lists(st.tuples(st.integers(min_value=0), st.just('debit')), min_size=1))
def test_ledger_balance_rollup_subtracts_amount_for_debit_entry(entries):
    computed_balance = ledger_balance_rollup(entries)
    expected_balance = sum(-amount for amount, kind in entries)
    assert computed_balance == expected_balance

@given(st.lists(st.tuples(st.integers(min_value=0), st.none()), min_size=1))
def test_ledger_balance_rollup_raises_value_error_for_unknown_kind(entries):
    try:
        ledger_balance_rollup(entries)
    except ValueError:
        assert True
    else:
        assert False

@given(st.lists(st.tuples(st.integers(), st.sampled_from(['credit', 'debit'])), min_size=1))
def test_ledger_balance_rollup_returns_balance(entries):
    computed_balance = ledger_balance_rollup(entries)
    assert isinstance(computed_balance, int) or isinstance(computed_balance, float)