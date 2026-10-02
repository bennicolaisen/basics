"""Facit till "Try It Yourself" i vecka 9. Förklaringarna finns i FACIT.md.

Bankens nya metoder ligger i subklassen FacitBank, så att veckans Bank
står kvar orörd. I ett riktigt projekt skulle de läggas direkt i Bank.
"""

from bank_simulation.account import BankAccount, InsufficientFundsError, SavingsAccount
from bank_simulation.bank import Bank


# Uppgift 1
class AccountNotEmptyError(Exception):
    """Raised when closing an account whose balance isn't exactly zero."""


# Uppgift 2
class CheckingAccount(BankAccount):
    """Ett konto som får gå minus, ner till -overdraft_limit."""

    def __init__(self, owner: str, balance: float = 0.0, overdraft_limit: float = 0.0):
        super().__init__(owner, balance)
        if overdraft_limit < 0:
            raise ValueError(f"overdraft_limit must be >= 0, got {overdraft_limit}")
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"withdraw amount must be > 0, got {amount}")
        if amount > self._balance + self.overdraft_limit:
            raise InsufficientFundsError(
                f"cannot withdraw {amount}: balance {self._balance}, overdraft limit {self.overdraft_limit}"
            )
        self._balance -= amount


# Uppgift 3: kontot för själv bok över sina händelser.
class AccountWithHistory(BankAccount):
    def __init__(self, owner: str, balance: float = 0.0):
        super().__init__(owner, balance)
        self.history: list[tuple[str, float, float]] = []

    def deposit(self, amount: float) -> None:
        super().deposit(amount)
        self.history.append(("deposit", amount, self.balance))

    def withdraw(self, amount: float) -> None:
        super().withdraw(amount)
        self.history.append(("withdraw", amount, self.balance))


class FacitBank(Bank):
    # Uppgift 1
    def close_account(self, account_id: str) -> BankAccount:
        account = self.get_account(account_id)
        if account.balance != 0:
            raise AccountNotEmptyError(
                f"account {account_id!r} still has {account.balance:.2f}; empty it before closing"
            )
        return self._accounts.pop(account_id)

    # Uppgift 3
    def statement(self, account_id: str) -> list[tuple[str, float, float]]:
        account = self.get_account(account_id)
        if not isinstance(account, AccountWithHistory):
            raise TypeError(f"account {account_id!r} does not keep a history")
        return list(account.history)

    # Uppgift 4: iterera över (id, konto)-par, som dict.items().
    def __iter__(self):
        return iter(self._accounts.items())

    # Uppgift 5: banken, inte kontot, vet när en månad är slut.
    def end_of_month(self) -> float:
        """Ge ränta på alla sparkonton. Returnerar summan av räntan."""
        total = 0.0
        for _, account in self:
            if isinstance(account, SavingsAccount):
                total += account.apply_interest()
        return total


class MonthlyInterestClock:
    """Känner till kalendern och säger till banken när en ny månad börjar."""

    def __init__(self, bank: FacitBank, year: int, month: int):
        self.bank = bank
        self.current = (year, month)

    def advance_to(self, year: int, month: int) -> int:
        """Flytta fram klockan och ge ränta för varje månad som avslutats. Returnerar antalet månader."""
        months = 0
        while self.current < (year, month):
            self.bank.end_of_month()
            current_year, current_month = self.current
            self.current = (current_year + current_month // 12, current_month % 12 + 1)
            months += 1
        return months
