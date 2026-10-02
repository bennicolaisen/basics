-- Uppgift 2: Antal snödagar per stad, 0 för städer utan snö, med LEFT JOIN
-- och utan CASE. Villkoret om snö står i ON, så städer utan snödagar
-- behåller en rad med NULL, och COUNT(o.id) räknar den som 0.
SELECT c.name,
       COUNT(o.id) AS snow_days
FROM cities c
LEFT JOIN observations o
       ON o.city_id = c.id
      AND o.conditions = 'snow'
GROUP BY c.id, c.name
ORDER BY c.name;
