import pytest

from bank_simulation.account import BankAccount, InsufficientFundsError, SavingsAccount


def test_deposit_increases_balance():
    account = BankAccount("Ada", 100)
    account.deposit(50)
    assert account.balance == 150


def test_deposit_rejects_non_positive_amount():
    account = BankAccount("Ada", 100)
    with pytest.raises(ValueError):
        account.deposit(0)
    with pytest.raises(ValueError):
        account.deposit(-10)


def test_withdraw_decreases_balance():
    account = BankAccount("Ada", 100)
    account.withdraw(40)
    assert account.balance == 60


def test_withdraw_rejects_non_positive_amount():
    account = BankAccount("Ada", 100)
    with pytest.raises(ValueError):
        account.withdraw(0)
    with pytest.raises(ValueError):
        account.withdraw(-5)


def test_withdraw_more_than_balance_raises_insufficient_funds():
    account = BankAccount("Ada", 100)
    with pytest.raises(InsufficientFundsError):
        account.withdraw(150)
    # Balance is untouched by the failed withdrawal.
    assert account.balance == 100


def test_negative_opening_balance_rejected():
    with pytest.raises(ValueError):
        BankAccount("Ada", -1)


def test_empty_owner_rejected():
    with pytest.raises(ValueError):
        BankAccount("", 100)


def test_str_contains_owner_and_balance():
    account = BankAccount("Grace", 42.5)
    text = str(account)
    assert "Grace" in text
    assert "42.5" in text


def test_eq_compares_owner_and_balance():
    a = BankAccount("Ada", 100)
    b = BankAccount("Ada", 100)
    c = BankAccount("Ada", 50)
    d = BankAccount("Grace", 100)
    assert a == b
    assert a != c
    assert a != d
    assert a != "not an account"


def test_savings_account_is_a_bank_account():
    savings = SavingsAccount("Ada", 100, interest_rate=0.05)
    assert isinstance(savings, BankAccount)
    savings.deposit(10)
    assert savings.balance == 110


def test_apply_interest_grows_balance_and_returns_amount_added():
    savings = SavingsAccount("Ada", 100, interest_rate=0.05)
    added = savings.apply_interest()
    assert added == pytest.approx(5.0)
    assert savings.balance == pytest.approx(105.0)


def test_negative_interest_rate_rejected():
    with pytest.raises(ValueError):
        SavingsAccount("Ada", 100, interest_rate=-0.01)
