-- Uppgift 3b: Matchar 'malmö' och 'MALMÖ'? 1 betyder ja, 0 betyder nej.
-- SQLite:s LIKE bryr sig inte om stora och små bokstäver, men BARA för
-- A-Z. M/m räknas som lika, Ö/ö gör det inte.
SELECT name,
       name LIKE 'malmö' AS lower_case_pattern,
       name LIKE 'MALMÖ' AS upper_case_pattern
FROM cities
WHERE id = 3;
