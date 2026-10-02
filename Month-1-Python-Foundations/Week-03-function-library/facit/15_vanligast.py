# Facit: Övning 3.15 – Det vanligaste värdet
#
# Genom att gå igenom värdena i sorterad ordning prövas de minsta först.
# Eftersom bästa värdet bara byts när ett värde förekommer fler gånger (>
# och inte >=) behåller det minsta platsen vid lika antal. Samma idé
# används i stats.mode.

def most_common(values: list[float]) -> float:
    if len(values) == 0:
        raise ValueError("listan är tom")
    best = values[0]
    best_count = 0
    for value in sorted(values):
        count = values.count(value)
        if count > best_count:
            best = value
            best_count = count
    return best
