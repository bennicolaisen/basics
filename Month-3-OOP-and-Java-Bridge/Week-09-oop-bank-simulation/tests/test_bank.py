import pytest

from bank_simulation.account import BankAccount, InsufficientFundsError
from bank_simulation.bank import AccountNotFoundError, Bank


def make_bank_with_two_accounts():
    bank = Bank("First Crash Course Bank")
    alice_id = bank.open_account(BankAccount("Alice", 100))
    bob_id = bank.open_account(BankAccount("Bob", 20))
    return bank, alice_id, bob_id


def test_open_account_returns_usable_id():
    bank = Bank("Test Bank")
    account_id = bank.open_account(BankAccount("Ada", 100))
    assert bank.get_account(account_id).owner == "Ada"


def test_get_account_missing_id_raises():
    bank = Bank("Test Bank")
    with pytest.raises(AccountNotFoundError):
        bank.get_account("does-not-exist")


def test_transfer_moves_money_between_accounts():
    bank, alice_id, bob_id = make_bank_with_two_accounts()
    bank.transfer(alice_id, bob_id, 30)
    assert bank.get_account(alice_id).balance == 70
    assert bank.get_account(bob_id).balance == 50


def test_transfer_insufficient_funds_leaves_both_accounts_unchanged():
    bank, alice_id, bob_id = make_bank_with_two_accounts()
    with pytest.raises(InsufficientFundsError):
        bank.transfer(alice_id, bob_id, 1000)
    assert bank.get_account(alice_id).balance == 100
    assert bank.get_account(bob_id).balance == 20


def test_transfer_invalid_amount_leaves_both_accounts_unchanged():
    bank, alice_id, bob_id = make_bank_with_two_accounts()
    with pytest.raises(ValueError):
        bank.transfer(alice_id, bob_id, -5)
    assert bank.get_account(alice_id).balance == 100
    assert bank.get_account(bob_id).balance == 20


def test_transfer_unknown_account_leaves_source_unchanged():
    bank, alice_id, _ = make_bank_with_two_accounts()
    with pytest.raises(AccountNotFoundError):
        bank.transfer(alice_id, "nope", 10)
    assert bank.get_account(alice_id).balance == 100


def test_total_assets_sums_all_accounts():
    bank, _, _ = make_bank_with_two_accounts()
    assert bank.total_assets() == 120
