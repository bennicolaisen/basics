# Facit: Övning 2.9 – Räkna vokaler
#
# text.lower() gör om allt till små bokstäver först, så att "Ö" och "ö"
# räknas lika utan att listan med vokaler behöver ha med både stora och
# små.

def count_vowels(text):
    count = 0
    for character in text.lower():
        if character in "aeiouyåäö":
            count = count + 1
    return count
