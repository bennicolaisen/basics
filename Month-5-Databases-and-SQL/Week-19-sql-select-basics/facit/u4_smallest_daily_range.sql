-- Uppgift 4: De tre observationerna med minst skillnad mellan högsta
-- och lägsta temperatur.
--
-- Två observationer delar tredjeplatsen (3.3). Utan fler kolumner i
-- ORDER BY är det inte bestämt vilken av dem som kommer med. Datum och
-- stad som extra sorteringsnycklar gör svaret förutsägbart.
SELECT observed_on, city_id, ROUND(temp_max_c - temp_min_c, 1) AS range_c
FROM observations
ORDER BY range_c, observed_on, city_id
LIMIT 3;
