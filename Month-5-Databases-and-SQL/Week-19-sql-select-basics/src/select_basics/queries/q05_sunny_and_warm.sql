-- Q05: Which days were sunny with a high of at least 15 degrees?
-- Concepts: AND (both conditions must hold), comparing text in 'single quotes'.
SELECT observed_on, city_id, temp_max_c
FROM observations
WHERE conditions = 'sun'
  AND temp_max_c >= 15;
