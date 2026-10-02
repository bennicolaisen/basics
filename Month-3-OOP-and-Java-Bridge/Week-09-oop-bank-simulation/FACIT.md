# Facit vecka 9 — Try It Yourself

Koden finns i [`facit/prova_sjalv.py`](facit/prova_sjalv.py) och testerna
i [`tests/test_facit.py`](tests/test_facit.py). Kör dem med
`python -m pytest` i veckans mapp.

Bankens nya metoder ligger i subklassen `FacitBank(Bank)`, så att veckans
`Bank` står kvar orörd. I ett riktigt projekt skulle de läggas direkt i
`Bank`.

## 1. Stänga ett konto

```python
class AccountNotEmptyError(Exception):
    """Raised when closing an account whose balance isn't exactly zero."""


def close_account(self, account_id):
    account = self.get_account(account_id)
    if account.balance != 0:
        raise AccountNotEmptyError(...)
    return self._accounts.pop(account_id)
```

Ett eget undantag gör att den som anropar kan skilja just det här felet
från andra: `except AccountNotEmptyError` fångar "kontot har pengar kvar"
men inte "kontot finns inte" (`AccountNotFoundError`, som `get_account`
redan kastar). Kontrollen sker **innan** något ändras, så ett nekat
försök lämnar kontot öppet; testet kontrollerar det. `dict.pop` både tar
bort kontot och returnerar det.

## 2. Ett konto som får gå minus

```python
class CheckingAccount(BankAccount):
    def __init__(self, owner, balance=0.0, overdraft_limit=0.0):
        super().__init__(owner, balance)
        ...
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError(...)
        if amount > self._balance + self.overdraft_limit:
            raise InsufficientFundsError(...)
        self._balance -= amount
```

Det enda som skiljer ett checkkonto från ett vanligt konto är **regeln
för hur mycket man får ta ut**. `deposit` ärvs oförändrad; bara
`withdraw` skrivs över (*override*). `super().__init__` låter
`BankAccount` sköta kontrollen av ägare och saldo, så den inte skrivs två
gånger.

En sak att lägga märke till: den nya `withdraw` upprepar kontrollen av
att beloppet är positivt. Det går att undvika med en liten ändring i
`BankAccount`: låt `withdraw` jämföra med en metod, till exempel
`available_funds()`, som returnerar saldot, och låt `CheckingAccount`
skriva över bara den metoden så att den returnerar saldot plus krediten.
Då innehåller subklassen exakt en rad med ny logik. Det mönstret (en
basklass som lämnar en liten, utbytbar del åt subklasserna) är vanligt;
det kallas *template method*. Facit ändrar inte veckans `BankAccount`, och
därför överskuggas hela `withdraw`.

## 3. Kontoutdrag

Var hör historiken hemma? **På kontot.** Det är kontot som vet när det
sätts in och tas ut pengar, så det är kontot som ska föra bok:

```python
class AccountWithHistory(BankAccount):
    def deposit(self, amount):
        super().deposit(amount)
        self.history.append(("deposit", amount, self.balance))

    def withdraw(self, amount):
        super().withdraw(amount)
        self.history.append(("withdraw", amount, self.balance))
```

Raden läggs till **efter** anropet till `super()`. Om uttaget nekas kastar
`super().withdraw` ett undantag och raden nås aldrig, så misslyckade
uttag hamnar inte i historiken. En överföring syns automatiskt som ett
uttag på det ena kontot och en insättning på det andra, eftersom
`Bank.transfer` använder `withdraw` och `deposit`. `statement` hämtar bara
kontots historik och returnerar en kopia, så att den som anropar inte kan
ändra den.

Om banken i stället förde boken skulle insättningar som görs direkt på
kontot (`account.deposit(50)`) missas.

## 4. Gör banken itererbar

```python
def __iter__(self):
    return iter(self._accounts.items())
```

Facit låter `for account_id, account in bank:` ge **par av id och konto**,
precis som `dict.items()`. Skälet: bankens övriga metoder (`transfer`,
`close_account`, `statement`) tar ett id, så den som går igenom kontona
behöver ofta id:t för att kunna göra något med kontot. Att bara ge
kontona tappar id:t, och att bara ge id:n tvingar fram ett extra
`get_account` för varje konto. Paret ger båda.

## 5. Ränta en gång i månaden

Konstruktionen är att **kontot inte ska veta vad en kalender är**. Ett
sparkonto vet hur man räknar ränta (`apply_interest`), men inte när det
ska ske. Ansvaret delas upp:

- **Banken** vet vilka konton den har och kan ge ränta till alla
  sparkonton på en gång: `end_of_month()`.
- **En klocka** (`MonthlyInterestClock`) vet vilken månad det är, och
  säger till banken en gång för varje månad som passerat.

```python
def advance_to(self, year, month):
    months = 0
    while self.current < (year, month):
        self.bank.end_of_month()
        current_year, current_month = self.current
        self.current = (current_year + current_month // 12, current_month % 12 + 1)
        months += 1
    return months
```

Månader lagras som tupler `(år, månad)`, som jämförs i rätt ordning
eftersom tupler jämförs ett värde i taget. Uppdelningen gör varje del
lätt att testa: testet flyttar klockan tre månader framåt utan att vänta
tre månader. I ett riktigt system skulle en schemalagd körning (ett jobb
som startar varje månad) anropa `end_of_month`.
