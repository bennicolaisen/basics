-- Q09: Stockholm's (city_id 1) readings from Wednesday to Friday, in date order.
-- Concepts: BETWEEN (inclusive on both ends), ISO dates compared as text, ORDER BY.
SELECT observed_on, temp_max_c, temp_min_c, conditions
FROM observations
WHERE city_id = 1
  AND observed_on BETWEEN '2026-09-23' AND '2026-09-25'
ORDER BY observed_on;
