"""Facit till "Try It Yourself" i vecka 5. Förklaringarna finns i FACIT.md."""


# Uppgift 1: spåra fibonacci(6). Svaret står i FACIT.md; funktionen här
# skriver ut samma spår, så att du kan jämföra med ditt eget.
def fibonacci_trace(n: int, depth: int = 0) -> int:
    indent = "  " * depth
    print(f"{indent}fibonacci({n})")
    if n < 2:
        print(f"{indent}-> {n}")
        return n
    result = fibonacci_trace(n - 1, depth + 1) + fibonacci_trace(n - 2, depth + 1)
    print(f"{indent}-> {result}")
    return result


# Uppgift 2: räkna anropen med en räknare på modulnivå.
call_count = 0


def fibonacci_counted(n: int) -> int:
    global call_count
    call_count += 1
    if n < 2:
        return n
    return fibonacci_counted(n - 1) + fibonacci_counted(n - 2)


# Uppgift 3: memoisering med en dictionary som cache.
memo_call_count = 0


def fibonacci_memo(n: int, cache: dict[int, int] | None = None) -> int:
    global memo_call_count
    memo_call_count += 1
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n}")
    if cache is None:
        cache = {}
    if n in cache:
        return cache[n]
    if n < 2:
        result = n
    else:
        result = fibonacci_memo(n - 1, cache) + fibonacci_memo(n - 2, cache)
    cache[n] = result
    return result


# Uppgift 4: factorial med ackumulator. Multiplikationen sker före det
# rekursiva anropet, så när basfallet nås är svaret redan klart.
def factorial_acc(n: int, acc: int = 1) -> int:
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n}")
    if n == 0:
        return acc
    return factorial_acc(n - 1, acc * n)


# Uppgift 5: skriv ut 1..n utan loop. Anropet kommer före utskriften, så
# de små talen skrivs ut först, på vägen tillbaka.
def count_up(n: int) -> None:
    if n <= 0:
        return
    count_up(n - 1)
    print(n)
