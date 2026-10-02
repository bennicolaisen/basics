# Facit: Övning 2.10 – Baklänges
#
# Varje nytt tecken läggs först i result, så det första tecknet hamnar
# sist. Kortare: return text[::-1], där steget -1 betyder "gå baklänges".

def reverse_text(text):
    result = ""
    for character in text:
        result = character + result
    return result
