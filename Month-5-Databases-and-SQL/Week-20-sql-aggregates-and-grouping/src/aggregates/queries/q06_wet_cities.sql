-- Q06: Which cities got more than 20 mm over the week? Wettest first.
-- Concepts: HAVING filters groups after they're built, so it can use aggregates.
SELECT city_id,
       ROUND(SUM(precipitation_mm), 1) AS total_mm
FROM observations
GROUP BY city_id
HAVING SUM(precipitation_mm) > 20
ORDER BY total_mm DESC;
