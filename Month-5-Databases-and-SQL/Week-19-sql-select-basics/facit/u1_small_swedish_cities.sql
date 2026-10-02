-- Uppgift 1: Svenska städer med färre än 200 000 invånare, störst först.
SELECT name, population
FROM cities
WHERE country = 'Sweden'
  AND population < 200000
ORDER BY population DESC;
