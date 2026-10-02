# Facit: Övning 2.16 – FizzBuzz
#
# "Delbart med både 3 och 5" måste kontrolleras först. Annars fångas 15
# redan av "delbart med 3" och blir "Fizz". Delbart med både 3 och 5 är
# samma sak som delbart med 15.

def fizzbuzz(n):
    result = []
    for number in range(1, n + 1):
        if number % 15 == 0:
            result.append("FizzBuzz")
        elif number % 3 == 0:
            result.append("Fizz")
        elif number % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(number))
    return result
