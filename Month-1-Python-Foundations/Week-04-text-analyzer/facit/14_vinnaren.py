# Facit: Övning 4.14 – Högst poäng
#
# sorted(scores) ger nycklarna (namnen) i bokstavsordning, och eftersom
# bästa namnet bara byts vid strikt fler poäng behåller det första namnet
# platsen vid lika poäng.

def winner(scores: dict[str, int]) -> str:
    best_name = None
    for name in sorted(scores):
        if best_name is None or scores[name] > scores[best_name]:
            best_name = name
    return best_name
