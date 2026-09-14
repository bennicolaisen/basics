"""Bank: an object composed of accounts, not related to them by inheritance.

A Bank HAS accounts — that's composition. It is not, and should not be, a
kind of BankAccount itself (no IS-A relationship makes sense here). See the
README's Concepts Refresher for why that distinction matters.
"""

from .account import BankAccount


class AccountNotFoundError(Exception):
    """Raised when an account id doesn't exist in this bank."""


class Bank:
    """Holds many accounts, keyed by account id, and moves money between them."""

    def __init__(self, name: str):
        if not name or not name.strip():
            raise ValueError("name must be a non-empty string")
        self.name = name
        self._accounts: dict[str, BankAccount] = {}
        self._next_id = 1

    def open_account(self, account: BankAccount) -> str:
        """Register `account` with the bank and return its new account id."""
        account_id = str(self._next_id)
        self._next_id += 1
        self._accounts[account_id] = account
        return account_id

    def get_account(self, account_id: str) -> BankAccount:
        """Look up an account by id. Raises AccountNotFoundError if missing."""
        try:
            return self._accounts[account_id]
        except KeyError:
            raise AccountNotFoundError(f"no account with id {account_id!r}") from None

    def transfer(self, from_id: str, to_id: str, amount: float) -> None:
        """Move `amount` from one account to another.

        All-or-nothing: if the withdrawal fails (insufficient funds or a
        bad amount), the deposit never happens and neither account changes.
        """
        source = self.get_account(from_id)
        destination = self.get_account(to_id)

        source.withdraw(amount)  # raises ValueError/InsufficientFundsError; nothing mutated yet
        try:
            destination.deposit(amount)
        except Exception:
            # Roll back the withdrawal so a failed deposit never leaves the
            # transfer half-done.
            source.deposit(amount)
            raise

    def total_assets(self) -> float:
        """Sum of every account's balance in this bank."""
        return sum(account.balance for account in self._accounts.values())
