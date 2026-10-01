"""DÅLIGT EXEMPEL: härma inte den här filen.

En enda stor funktion med korta, otydliga namn som gör allt på en gång:
räknar statistik, analyserar text och skriver ut. Den fungerar, men den
går inte att testa en del i taget och inget i den kan återanvändas.
Uppgift 1 i "Prova själv" går ut på att dela upp den i anrop till
stats.py och text_utils.py. Den har inga tester, med flit.
"""


def handle_data(d, t):
    s = 0
    c = 0
    for x in d:
        s = s + x
        c = c + 1
    avg = s / c

    sd = sorted(d)
    n = len(sd)
    if n % 2 == 0:
        med = (sd[n // 2 - 1] + sd[n // 2]) / 2
    else:
        med = sd[n // 2]

    best = None
    bc = -1
    for x in sd:
        k = 0
        for y in d:
            if y == x:
                k = k + 1
        if k > bc:
            bc = k
            best = x

    v = 0
    for x in d:
        v = v + (x - avg) ** 2
    dev = (v / c) ** 0.5

    w = len(t.split())

    cl = ""
    for ch in t:
        if ch != " ":
            cl = cl + ch
    cl = cl.lower()
    p = cl == cl[::-1]

    print("=== Rapport ===")
    print("Medelvärde:", avg)
    print("Median:", med)
    print("Typvärde:", best)
    print("Standardavvikelse:", dev)
    print("Antal ord:", w)
    print("Palindrom:", p)
