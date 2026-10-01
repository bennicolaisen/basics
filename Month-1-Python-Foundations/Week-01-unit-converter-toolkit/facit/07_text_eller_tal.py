# Facit: Övning 1.7 – Text eller tal?
#
# "10" och "5" står inom citattecken, så de är text (str), inte tal. För
# text betyder + "sätt ihop", så "10" + "5" blir "105". int() gör om
# texten till heltal, och för tal betyder + addition.

a = "10"
b = "5"
print(int(a) + int(b))
