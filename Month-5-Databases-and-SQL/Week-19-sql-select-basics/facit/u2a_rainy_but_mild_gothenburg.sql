-- Uppgift 2a: Dagar i Göteborg (city_id 2) med regn där
-- dagens högsta ändå nådde 14 grader.
SELECT id, observed_on, temp_max_c, conditions
FROM observations
WHERE city_id = 2
  AND conditions = 'rain'
  AND temp_max_c >= 14;
