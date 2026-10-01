# Facit: Övning 4.18 – Din första klass
#
# __init__ körs när objektet skapas och sparar värdena i self, som är
# objektet självt. Metoderna läser dem sedan via self.width och
# self.height. Jämför med övning 1.15, där bredd och höjd fick skickas in
# till varje funktion: här bär objektet sina egna värden.

class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def is_square(self) -> bool:
        return self.width == self.height
