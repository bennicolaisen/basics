-- Q06: How many observations does every city have, including cities with none?
-- Concepts: LEFT JOIN + GROUP BY, and COUNT(o.id) rather than COUNT(*).
SELECT c.name,
       COUNT(o.id) AS observations
FROM cities AS c
LEFT JOIN observations AS o ON o.city_id = c.id
GROUP BY c.id, c.name
ORDER BY observations DESC, c.name;
