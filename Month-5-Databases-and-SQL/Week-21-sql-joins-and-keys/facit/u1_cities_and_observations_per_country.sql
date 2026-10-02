-- Uppgift 1: Varje land med antal städer och antal observationer,
-- Danmark med 0 observationer inräknat.
--
-- Efter joinen finns en rad per (stad, observation), så Sverige har 42
-- rader. COUNT(DISTINCT c.id) räknar städerna en gång var; COUNT(o.id)
-- räknar observationerna och hoppar över NULL, så Köpenhamns tomma rad
-- blir 0.
SELECT c.country,
       COUNT(DISTINCT c.id) AS cities,
       COUNT(o.id)          AS observations
FROM cities c
LEFT JOIN observations o ON o.city_id = c.id
GROUP BY c.country
ORDER BY c.country;
