-- Uppgift 3: Städer där även veckans LÄGSTA dagstemperatur (temp_max_c)
-- låg över 13 grader. Villkoret gäller en hel grupp (MIN över veckan), så
-- det hör hemma i HAVING.
SELECT city_id,
       MIN(temp_max_c) AS lowest_high_c
FROM observations
GROUP BY city_id
HAVING MIN(temp_max_c) > 13
ORDER BY city_id;
