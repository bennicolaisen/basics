-- Q04: Average daily precipitation per country.
-- Concepts: grouping by a column that only exists in the other table.
SELECT c.country,
       COUNT(*)                          AS observations,
       ROUND(AVG(o.precipitation_mm), 2) AS average_daily_mm
FROM observations AS o
JOIN cities AS c ON c.id = o.city_id
GROUP BY c.country
ORDER BY c.country;
