# Facit: Övning 2.3 – Betyg
#
# Ordningen spelar roll. Om man börjar med points >= 50 skulle 95 bli "E",
# eftersom den första sanna grenen körs och resten hoppas över. Genom att
# börja uppifrån behöver ingen gren ange en övre gräns.

def grade(points):
    if points >= 90:
        return "A"
    elif points >= 80:
        return "B"
    elif points >= 70:
        return "C"
    elif points >= 60:
        return "D"
    elif points >= 50:
        return "E"
    else:
        return "F"
