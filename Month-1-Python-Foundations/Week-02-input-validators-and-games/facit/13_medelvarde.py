# Facit: Övning 2.13 – Medelvärde och tomma listor
#
# Utan kontrollen skulle en tom lista ge ZeroDivisionError (0 / 0), som
# inte säger något om vad som gick fel. Ett eget ValueError med ett
# tydligt meddelande gör felet lätt att förstå.

def average(numbers):
    if len(numbers) == 0:
        raise ValueError("listan är tom")
    return sum(numbers) / len(numbers)
