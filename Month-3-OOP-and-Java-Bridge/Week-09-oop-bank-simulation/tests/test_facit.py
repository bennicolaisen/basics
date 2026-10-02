"""Tests for the Try It Yourself solutions in facit/prova_sjalv.py."""

import pytest

from bank_simulation.account import BankAccount, InsufficientFundsError, SavingsAccount
from bank_simulation.bank import AccountNotFoundError
from facit import prova_sjalv as facit


class TestCloseAccount:
    def test_empty_account_closes(self):
        bank = facit.FacitBank("Banken")
        account_id = bank.open_account(BankAccount("Alva"))
        bank.close_account(account_id)
        with pytest.raises(AccountNotFoundError):
            bank.get_account(account_id)

    def test_account_with_money_is_refused_and_stays_open(self):
        bank = facit.FacitBank("Banken")
        account_id = bank.open_account(BankAccount("Alva", 10))
        with pytest.raises(facit.AccountNotEmptyError):
            bank.close_account(account_id)
        assert bank.get_account(account_id).balance == 10

    def test_unknown_account(self):
        with pytest.raises(AccountNotFoundError):
            facit.FacitBank("Banken").close_account("99")


class TestCheckingAccount:
    def test_can_go_negative_down_to_the_limit(self):
        account = facit.CheckingAccount("Bo", 100, overdraft_limit=50)
        account.withdraw(150)
        assert account.balance == -50

    def test_cannot_go_past_the_limit(self):
        account = facit.CheckingAccount("Bo", 100, overdraft_limit=50)
        with pytest.raises(InsufficientFundsError):
            account.withdraw(150.01)
        assert account.balance == 100

    def test_deposit_is_inherited_unchanged(self):
        account = facit.CheckingAccount("Bo", 0, overdraft_limit=50)
        account.withdraw(30)
        account.deposit(40)
        assert account.balance == 10

    def test_is_still_a_bank_account(self):
        assert isinstance(facit.CheckingAccount("Bo"), BankAccount)

    def test_negative_limit_rejected(self):
        with pytest.raises(ValueError):
            facit.CheckingAccount("Bo", 0, overdraft_limit=-1)


class TestStatement:
    def test_records_deposits_withdrawals_and_transfers(self):
        bank = facit.FacitBank("Banken")
        alva = bank.open_account(facit.AccountWithHistory("Alva", 100))
        bo = bank.open_account(facit.AccountWithHistory("Bo"))
        bank.get_account(alva).deposit(50)
        bank.transfer(alva, bo, 30)
        assert bank.statement(alva) == [("deposit", 50, 150.0), ("withdraw", 30, 120.0)]
        assert bank.statement(bo) == [("deposit", 30, 30.0)]

    def test_failed_withdrawal_is_not_recorded(self):
        account = facit.AccountWithHistory("Alva", 10)
        with pytest.raises(InsufficientFundsError):
            account.withdraw(20)
        assert account.history == []


def test_bank_is_iterable_as_id_account_pairs():
    bank = facit.FacitBank("Banken")
    first = bank.open_account(BankAccount("Alva"))
    second = bank.open_account(BankAccount("Bo"))
    assert [(account_id, account.owner) for account_id, account in bank] == [(first, "Alva"), (second, "Bo")]


class TestMonthlyInterest:
    def test_end_of_month_pays_interest_on_savings_only(self):
        bank = facit.FacitBank("Banken")
        savings = bank.open_account(SavingsAccount("Alva", 1000, interest_rate=0.01))
        plain = bank.open_account(BankAccount("Bo", 1000))
        assert bank.end_of_month() == pytest.approx(10.0)
        assert bank.get_account(savings).balance == pytest.approx(1010.0)
        assert bank.get_account(plain).balance == 1000

    def test_clock_applies_interest_once_per_completed_month(self):
        bank = facit.FacitBank("Banken")
        savings = bank.open_account(SavingsAccount("Alva", 1000, interest_rate=0.01))
        clock = facit.MonthlyInterestClock(bank, 2026, 11)
        assert clock.advance_to(2027, 2) == 3  # november, december, januari
        assert clock.current == (2027, 2)
        assert bank.get_account(savings).balance == pytest.approx(1000 * 1.01 ** 3)
        assert clock.advance_to(2027, 2) == 0
