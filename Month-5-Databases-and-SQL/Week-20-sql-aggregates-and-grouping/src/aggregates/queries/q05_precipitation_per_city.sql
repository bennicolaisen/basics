-- Q05: Total precipitation for each city (by city_id), wettest first.
-- Concepts: GROUP BY a column, aggregate the rest.
SELECT city_id,
       ROUND(SUM(precipitation_mm), 1) AS total_mm
FROM observations
GROUP BY city_id
ORDER BY total_mm DESC;
