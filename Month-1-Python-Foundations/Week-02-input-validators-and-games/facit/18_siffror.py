# Facit: Övning 2.18 – Bara siffror?
#
# is_postcode tar bara bort mellanslaget om det står på rätt plats (index
# 3, det fjärde tecknet, eftersom index börjar på 0). Sedan räcker det att
# kontrollera att det är exakt fem tecken och att alla är siffror.

def count_digits(text):
    count = 0
    for character in text:
        if character.isdigit():
            count = count + 1
    return count


def is_postcode(text):
    if len(text) == 6 and text[3] == " ":
        text = text.replace(" ", "", 1)
    return len(text) == 5 and text.isdigit()
