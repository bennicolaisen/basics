-- Q02: Where and when did it snow?
-- Concepts: WHERE on a joined query can filter on either table's columns.
SELECT c.name,
       o.observed_on,
       o.temp_max_c,
       o.temp_min_c
FROM observations AS o
JOIN cities AS c ON c.id = o.city_id
WHERE o.conditions = 'snow'
ORDER BY o.observed_on;
