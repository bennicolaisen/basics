# Övning 3.14 – Skriv egna tester
#
# Nu är det du som skriver testerna. Funktionen is_palindrome i veckans
# projekt (src/function_library/text_utils.py) importeras nedan. Skriv
# minst tre testfunktioner för den, i den här filen.
#
# Kontrollen kör dina tester två gånger: först mot den riktiga funktionen
# (då ska alla gå igenom), och sedan mot tre felaktiga versioner. Dina
# tester måste avslöja alla tre: för varje felaktig version ska minst ett
# av dina tester misslyckas.
#
# Fundera på: vad händer med stora bokstäver, mellanslag, och parametrarna
# ignore_case och ignore_spaces?
#
# Kontrollera: python -m pytest kontroll -k 14

from function_library.text_utils import is_palindrome


def test_simple_palindrome():
    assert is_palindrome("kajak")


# Skriv fler tester här. Varje testfunktion ska börja med test_.
