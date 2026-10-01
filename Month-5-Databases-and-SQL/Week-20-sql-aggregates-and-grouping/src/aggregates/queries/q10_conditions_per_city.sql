-- Q10: For each city, how many days of each kind of weather did it get?
-- Concepts: GROUP BY two columns: one group per distinct (city_id, conditions) pair.
SELECT city_id,
       conditions,
       COUNT(*) AS days
FROM observations
GROUP BY city_id, conditions
ORDER BY city_id, conditions;
