# Week 9 — OOP in Python: A Bank Simulation

## Purpose

Every project so far has been *procedural*: data in variables, functions
that operate on that data, passed around explicitly. That works, but it
starts to strain once a program has several kinds of thing (accounts,
customers, a bank) that each carry their own state and their own rules for
changing that state safely. Object-oriented programming is the answer to
that strain: bundle state and the behavior that's allowed to touch it into
one unit, and let objects hand off work to each other instead of one big
function juggling everything. A bank is a natural example — accounts have
rules (never go negative), and a transfer between two accounts has to
either fully happen or not happen at all.

## Objectives

The code in this project demonstrates:

- Defining a class with `__init__`, instance attributes, and methods.
- Encapsulation: routing every change to an account's balance through
  `deposit`/`withdraw` instead of letting external code touch the balance
  directly, and what "internal" means in Python without a `private`
  keyword.
- A custom exception (`InsufficientFundsError`) for a domain-specific
  failure that plain `ValueError` doesn't describe well.
- Composition: `Bank` *has* accounts — it manages a collection of them, it
  isn't one itself.
- A light, real use of inheritance (`SavingsAccount(BankAccount)`) as a
  preview of what Week 11 covers properly in Java.
- Overriding `__str__` and `__eq__` so objects print and compare the way a
  human expects instead of Python's default identity-based behavior.
- An all-or-nothing operation (`Bank.transfer`) that rolls back its first
  step if its second step fails.

## Concepts Refresher

### What an object actually is

An **object** is state and behavior bundled together. `BankAccount` isn't
just a record with an `owner` and a `balance` field — the *only* sanctioned
way to change that balance is through the object's own methods
(`deposit`/`withdraw`). Compare that to Month 1–2 code, where a function
like `apply_discount(price, percent)` had no memory of anything; it took
values in and returned a value out, and any "state" lived in whatever
variable the caller kept it in. An object keeps its own state across many
method calls — a `BankAccount` remembers its balance for as long as it
exists, and every method call sees whatever the last call left behind.

```python
account = BankAccount("Ada", 100)
account.deposit(50)     # account remembers this happened
account.withdraw(20)
print(account.balance)  # 130 — state persisted across three separate calls
```

### Encapsulation — and the reverse confusion from Java

Encapsulation means **controlling access to an object's state through its
methods**, so the object can enforce its own rules (a balance can never go
negative; an amount must be positive). It does **not** mean the language
physically hides the memory from you. In Python, `account._balance` is
completely reachable — nothing stops you from writing
`account._balance = -999` and corrupting the account's invariant.

The leading underscore in `_balance` is a **convention**, not a lock:
it's Python programmers universally agreeing "this is internal, other code
shouldn't touch it, even though the language will let you." If you've seen
Java's `private` keyword, this is the opposite failure mode from what you'd
expect there: Java's `private` is enforced by the compiler — code outside
the class genuinely cannot compile a reference to a private field. Python
has no such keyword at all. Discipline replaces enforcement. (Week 10
covers Java's actual access modifiers when you get there.)

### Composition: `Bank` HAS-A `BankAccount`

`Bank` doesn't inherit from `BankAccount` — there's no sense in which a
bank *is a kind of* account. Instead, a `Bank` **has** many accounts: it
holds a dictionary of them and exposes operations (`open_account`,
`transfer`) that work *in terms of* the accounts it holds, by calling
their own `deposit`/`withdraw` methods rather than reaching into their
balances directly. This relationship — "object A holds references to
object(s) B and delegates to them" — is called **composition**, and it's
usually the right default when you're tempted to reach for inheritance.
Week 11 introduces the other relationship, **inheritance** ("IS-A"), and
contrasts the two directly — keep this HAS-A example in mind when you get
there.

### Why `__eq__` and `__str__` need overriding

Every Python object automatically gets a `__str__` (used by `print()`) and
an `__eq__` (used by `==`) — you just probably haven't noticed, because the
defaults are rarely what you want:

```python
class Empty:
    pass

a, b = Empty(), Empty()
print(a)       # <__main__.Empty object at 0x7f...>  — not useful
print(a == b)  # False — compares object *identity*, not content
```

By default, `__eq__` compares **identity** (are these two variables the
exact same object in memory?), and `__str__` prints a memory address. That
means two `BankAccount("Ada", 100)` objects — same owner, same balance —
would compare unequal unless `__eq__` is overridden to compare their
actual data instead of their identity. Same story for `__str__`: without
overriding it, `print(account)` would print something useless instead of
`"Ada's account: 100.00"`. These are called **dunder methods** ("double
underscore") — Python's mechanism for making a class participate in
built-in operations (`==`, `print()`, `+`, `len()`, and more) by giving it
a method with a special reserved name that Python calls automatically.

### A preview of inheritance

`SavingsAccount(BankAccount)` means "a `SavingsAccount` IS-A
`BankAccount`, plus an `interest_rate` and an `apply_interest()` method."
It reuses everything `BankAccount` already does (`deposit`, `withdraw`,
`__str__`, `__eq__` unless overridden) and adds to it, via
`super().__init__(...)` in its own constructor. This is a real, working
example — but the *rules* around inheritance (what can be overridden, what
must be, abstract base behavior, polymorphism through a shared type) get
covered properly with Java in Week 11, where the language makes those
rules explicit and enforced instead of implicit and convention-based.

## Design & Architecture

```
src/bank_simulation/
├── __init__.py
├── account.py    — BankAccount, SavingsAccount, InsufficientFundsError
└── bank.py       — Bank, AccountNotFoundError
tests/
├── test_account.py
└── test_bank.py
```

`account.py` owns everything about a single account acting alone —
balance rules, interest, equality/printing. `bank.py` owns everything
about *multiple* accounts acting together — lookup by id, and transfers
that touch two accounts atomically. Nothing in `bank.py` reaches into an
account's `_balance` directly; it only calls `deposit`/`withdraw`, exactly
as external code should.

## How to Build & Run

No build step — this is plain Python using only the standard library.

```bash
cd Month-3-OOP-and-Java-Bridge/Week-09-oop-bank-simulation
python3 -m pytest -q
```

To poke at it interactively:

```bash
python3 -c "
from bank_simulation.bank import Bank
from bank_simulation.account import BankAccount, SavingsAccount

bank = Bank('Crash Course Bank')
a = bank.open_account(BankAccount('Ada', 100))
b = bank.open_account(SavingsAccount('Grace', 200, interest_rate=0.03))
bank.transfer(a, b, 25)
print(bank.get_account(a))
print(bank.get_account(b))
"
```

## Testing

`conftest.py` adds `src/` to `sys.path` so `pytest` runs with zero extra
flags from this directory.

Covered:

- `BankAccount`: deposit/withdraw happy paths, `InsufficientFundsError` on
  overdraw, `ValueError` on non-positive amounts and invalid construction,
  `__str__` content, `__eq__` behavior (equal state, different state,
  wrong type).
- `SavingsAccount`: is a `BankAccount`, interest calculation, rejects a
  negative rate.
- `Bank`: opening accounts and looking them up, unknown-id lookup,
  successful transfer, and — the important edge case — a failed transfer
  (insufficient funds, invalid amount, or unknown account) leaving **both**
  accounts exactly as they were before the attempt.

```bash
python3 -m pytest -q
```

## Try It Yourself

> **Facit (answer key):** every exercise below is solved, tested and explained
> in Swedish in [FACIT.md](FACIT.md). Try each one yourself first, then compare.

1. Add a `close_account(account_id)` to `Bank` that only succeeds if the
   account's balance is exactly zero, otherwise raises an exception of
   your own design.
2. Add a `CheckingAccount(BankAccount)` that allows the balance to go
   negative up to an `overdraft_limit`, without duplicating
   `deposit`/`withdraw` — think about exactly which method needs to change
   and which can stay inherited as-is.
3. Give `Bank` a `statement(account_id)` method that returns a running
   transaction history (you'll need to record deposits/withdrawals/
   transfers somewhere — where does that state naturally belong?).
4. Make `Bank` itself iterable (`for account in bank: ...`) by implementing
   `__iter__`. What should it yield — the accounts, the ids, or `(id,
   account)` pairs? Justify your choice.
5. `SavingsAccount.apply_interest()` currently must be called manually.
   Design (on paper first) how you'd model "interest applies automatically
   once per month" without the class needing to know what a calendar is —
   what object would own that responsibility instead?
