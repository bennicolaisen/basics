-- Uppgift 5: Helgens observationer (26-27 september) där vinden är känd
-- och under 3 m/s.
SELECT id, observed_on, city_id, wind_ms
FROM observations
WHERE observed_on IN ('2026-09-26', '2026-09-27')
  AND wind_ms IS NOT NULL
  AND wind_ms < 3
ORDER BY observed_on, city_id;
