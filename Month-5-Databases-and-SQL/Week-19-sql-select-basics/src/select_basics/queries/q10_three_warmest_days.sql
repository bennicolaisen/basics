-- Q10: The three highest daily highs of the week, warmest first.
-- Concepts: ORDER BY ... DESC, LIMIT.
SELECT observed_on, city_id, temp_max_c
FROM observations
ORDER BY temp_max_c DESC
LIMIT 3;
