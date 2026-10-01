# Övning 2.18 – Bara siffror?
#
# Skriv klart två funktioner:
#
# count_digits(text) ska returnera hur många tecken i texten som är
# siffror. count_digits("Box 123, 456 Umeå") ska ge 6.
#
# is_postcode(text) ska returnera True om texten är ett svenskt postnummer
# skrivet som fem siffror, eventuellt med ett mellanslag efter de tre
# första: "90736" och "907 36" ska ge True, men "9073" och "907-36" ska ge
# False.
#
# Tips: "5".isdigit() är True. text.replace(" ", "", 1) tar bort det
# första mellanslaget.
#
# Kontrollera: python -m pytest kontroll -k 18

def count_digits(text):
    ...  # Byt ut ... mot din kod.


def is_postcode(text):
    ...  # Byt ut ... mot din kod.
