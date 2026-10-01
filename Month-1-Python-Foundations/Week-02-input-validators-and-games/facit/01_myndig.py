# Facit: Övning 2.1 – Myndig?
#
# Man kan skriva if age >= 18: return True else: return False, men
# jämförelsen age >= 18 är redan ett bool-värde. Att returnera den direkt
# är kortare och lika tydligt.

def is_adult(age):
    return age >= 18
