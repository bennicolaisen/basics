# Facit: Övning 2.11 – Största talet
#
# Att börja med biggest = 0 vore ett vanligt fel: för en lista med bara
# negativa tal skulle svaret bli 0, som inte ens finns i listan. Att börja
# med det första talet fungerar alltid.

def largest(numbers):
    biggest = numbers[0]
    for number in numbers:
        if number > biggest:
            biggest = number
    return biggest
