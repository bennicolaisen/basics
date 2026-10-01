"""Statistik för en lista med tal: medelvärde, median, typvärde och standardavvikelse.

Alla funktioner kastar ValueError om listan är tom. En tom lista har
inget medelvärde, och att returnera 0 eller None i stället skulle bara
låta ett felaktigt svar smita vidare i programmet.
"""


def mean(numbers: list[float]) -> float:
    """Medelvärdet: summan delat med antalet."""
    if len(numbers) == 0:
        raise ValueError("mean() behöver minst ett tal")
    return sum(numbers) / len(numbers)


def median(numbers: list[float]) -> float:
    """Det mittersta talet när listan är sorterad.

    Med ett jämnt antal tal finns två mittersta, och då är medianen
    medelvärdet av dem.
    """
    if len(numbers) == 0:
        raise ValueError("median() behöver minst ett tal")
    ordered = sorted(numbers)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def mode(numbers: list[float]) -> float:
    """Typvärdet: det tal som förekommer flest gånger.

    Om flera tal förekommer lika många gånger returneras det minsta av
    dem, så att svaret alltid blir detsamma för samma lista.
    """
    if len(numbers) == 0:
        raise ValueError("mode() behöver minst ett tal")
    best = numbers[0]
    best_count = 0
    # sorted() gör att de minsta talen prövas först. Eftersom vi bara byter
    # när ett tal förekommer *fler* gånger vinner det minsta vid lika antal.
    for value in sorted(numbers):
        count = numbers.count(value)
        if count > best_count:
            best = value
            best_count = count
    return best


def stddev(numbers: list[float]) -> float:
    """Standardavvikelsen: hur mycket talen i genomsnitt avviker från medelvärdet.

    Det här är populationens standardavvikelse (dela med antalet tal). Det
    finns också en variant för stickprov som delar med antalet minus ett;
    den används när talen bara är ett urval ur en större mängd.
    """
    average = mean(numbers)
    total = 0
    for value in numbers:
        total = total + (value - average) ** 2
    return (total / len(numbers)) ** 0.5
