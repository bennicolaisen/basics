"""BankAccount and SavingsAccount: the core objects of the simulation.

Both classes bundle state (owner, balance) with the behavior that's allowed
to touch that state (deposit, withdraw). Nothing outside this module is
supposed to reach in and mutate `_balance` directly — see the README's
Concepts Refresher for why that's a *convention* in Python, not a wall the
language enforces the way `private` would in Java.
"""


class InsufficientFundsError(Exception):
    """Raised when a withdrawal would take the balance below zero."""


class BankAccount:
    """A bank account with an owner and a balance.

    The balance is tracked in `_balance`. The single leading underscore is
    Python's convention for "internal — don't touch this from outside the
    class", not a language-enforced restriction. See the README.
    """

    def __init__(self, owner: str, balance: float = 0.0):
        if not owner or not owner.strip():
            raise ValueError("owner must be a non-empty string")
        if balance < 0:
            raise ValueError(f"balance must be >= 0, got {balance}")
        self.owner = owner
        self._balance = float(balance)

    @property
    def balance(self) -> float:
        """Read-only view of the current balance."""
        return self._balance

    def deposit(self, amount: float) -> None:
        """Add `amount` to the balance. Rejects non-positive amounts."""
        if amount <= 0:
            raise ValueError(f"deposit amount must be > 0, got {amount}")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Remove `amount` from the balance.

        Raises ValueError for a non-positive amount, and
        InsufficientFundsError if `amount` exceeds the current balance.
        """
        if amount <= 0:
            raise ValueError(f"withdraw amount must be > 0, got {amount}")
        if amount > self._balance:
            raise InsufficientFundsError(
                f"cannot withdraw {amount} from balance {self._balance}"
            )
        self._balance -= amount

    def __str__(self) -> str:
        return f"{self.owner}'s account: {self._balance:.2f}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.owner == other.owner and self._balance == other._balance

    def __hash__(self) -> int:
        # Accounts are mutable (balance changes), so hashing by identity
        # keeps them usable in sets/dicts without pretending two accounts
        # with equal owner+balance right now must stay interchangeable
        # after a future deposit/withdraw.
        return id(self)


class SavingsAccount(BankAccount):
    """A BankAccount that also accrues interest.

    This is a light preview of inheritance: a SavingsAccount IS-A
    BankAccount plus one extra field and one extra method. Formal
    inheritance rules (abstract classes, interfaces, overriding rules,
    polymorphism) get covered properly with Java in Week 11 — this is just
    a real, working taste of it in a language you already know.
    """

    def __init__(self, owner: str, balance: float = 0.0, interest_rate: float = 0.01):
        super().__init__(owner, balance)
        if interest_rate < 0:
            raise ValueError(f"interest_rate must be >= 0, got {interest_rate}")
        self.interest_rate = interest_rate

    def apply_interest(self) -> float:
        """Add one period's interest to the balance; return the amount added."""
        interest = self._balance * self.interest_rate
        self._balance += interest
        return interest

    def __str__(self) -> str:
        return f"{self.owner}'s savings account: {self._balance:.2f} @ {self.interest_rate:.2%}"
