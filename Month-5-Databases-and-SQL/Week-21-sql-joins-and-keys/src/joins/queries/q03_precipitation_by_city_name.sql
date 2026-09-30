-- Q03: Week 20's precipitation-per-city query, with names instead of ids.
-- Concepts: JOIN then GROUP BY; grouping by the key (c.id) as well as the name.
SELECT c.name,
       ROUND(SUM(o.precipitation_mm), 1) AS total_mm
FROM observations AS o
JOIN cities AS c ON c.id = o.city_id
GROUP BY c.id, c.name
ORDER BY total_mm DESC;
