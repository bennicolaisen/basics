-- Q07: Which observations are missing a wind reading?
-- Concepts: NULL, and why it needs IS NULL instead of = NULL.
SELECT id, city_id, observed_on
FROM observations
WHERE wind_ms IS NULL;
