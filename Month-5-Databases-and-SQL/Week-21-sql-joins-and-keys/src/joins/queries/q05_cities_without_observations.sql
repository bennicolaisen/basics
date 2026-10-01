-- Q05: Which cities have no observations at all?
-- Concepts: LEFT JOIN keeps every city; the unmatched ones get NULL for every o.* column.
SELECT c.name
FROM cities AS c
LEFT JOIN observations AS o ON o.city_id = c.id
WHERE o.id IS NULL;
