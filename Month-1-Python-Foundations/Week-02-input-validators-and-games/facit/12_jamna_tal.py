# Facit: Övning 2.12 – Bara jämna tal

def only_even(numbers):
    result = []
    for number in numbers:
        if number % 2 == 0:
            result.append(number)
    return result
