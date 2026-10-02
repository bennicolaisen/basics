-- Uppgift 3a: Städer vars namn slutar på a.
-- % betyder "vilka tecken som helst, hur många som helst".
SELECT name
FROM cities
WHERE name LIKE '%a';
