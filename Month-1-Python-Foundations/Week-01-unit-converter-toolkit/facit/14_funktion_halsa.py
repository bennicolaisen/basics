# Facit: Övning 1.14 – return eller print?
#
# print() visar text på skärmen men lämnar inget svar tillbaka. return
# lämnar tillbaka svaret, så att andra delar av programmet (och testerna)
# kan använda det: spara det, jämföra det eller skriva ut det.

def greeting(name):
    return f"Hej, {name}!"
