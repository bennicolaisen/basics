-- Q07: On which day did each city reach its warmest high of the week?
-- Concepts: a subquery in FROM (a grouped result used as a table), joined back to the rows.
SELECT c.name,
       o.observed_on,
       o.temp_max_c
FROM observations AS o
JOIN cities AS c ON c.id = o.city_id
JOIN (
    SELECT city_id, MAX(temp_max_c) AS warmest_c
    FROM observations
    GROUP BY city_id
) AS best ON best.city_id = o.city_id
         AND best.warmest_c = o.temp_max_c
ORDER BY o.temp_max_c DESC;
