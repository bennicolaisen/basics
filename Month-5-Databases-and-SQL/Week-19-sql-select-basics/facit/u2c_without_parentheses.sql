-- Uppgift 2c: SAMMA fråga UTAN parentes, för att se felet.
-- AND binder hårdare än OR, så detta betyder
--   conditions = 'rain' OR (conditions = 'snow' AND temp_max_c < 10)
-- och ALLA regndagar kommer med, även Oslos varma.
SELECT id, city_id, observed_on, temp_max_c, conditions
FROM observations
WHERE conditions = 'rain' OR conditions = 'snow'
  AND temp_max_c < 10;
