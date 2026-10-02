# Övning 4.18 – Din första klass
#
# Skriv klart klassen Rectangle. Ett Rectangle-objekt skapas med
# Rectangle(3, 4) och ska spara bredden och höjden i attributen width och
# height. Det ska ha tre metoder:
#
#     area()       returnerar bredd gånger höjd
#     perimeter()  returnerar omkretsen
#     is_square()  returnerar True om bredd och höjd är lika
#
# r = Rectangle(3, 4) ska ge r.width == 3, r.area() == 12, r.perimeter()
# == 14 och r.is_square() == False.
#
# Kontrollera: python -m pytest kontroll -k 18

class Rectangle:
    def __init__(self, width, height):
        ...  # Spara width och height i self.

    def area(self):
        ...  # Byt ut ... mot din kod.

    def perimeter(self):
        ...  # Byt ut ... mot din kod.

    def is_square(self):
        ...  # Byt ut ... mot din kod.
