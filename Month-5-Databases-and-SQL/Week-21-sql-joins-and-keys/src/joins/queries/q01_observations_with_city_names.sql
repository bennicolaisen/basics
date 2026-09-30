-- Q01: Every observation with its city's name instead of a bare city_id.
-- Concepts: JOIN ... ON, table aliases (o, c), qualified column names.
SELECT c.name,
       o.observed_on,
       o.temp_max_c,
       o.conditions
FROM observations AS o
JOIN cities AS c ON c.id = o.city_id
ORDER BY c.name, o.observed_on;
