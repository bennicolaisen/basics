-- Q07: Which cities had at least three rainy days, and how many?
-- Concepts: WHERE (filter rows, before grouping) and HAVING (filter groups, after) together.
SELECT city_id,
       COUNT(*) AS rainy_days
FROM observations
WHERE conditions = 'rain'
GROUP BY city_id
HAVING COUNT(*) >= 3
ORDER BY city_id;
