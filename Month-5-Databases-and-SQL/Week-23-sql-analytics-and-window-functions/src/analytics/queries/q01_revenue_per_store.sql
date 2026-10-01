-- Q01: Total revenue and units for each store, with its city name, highest revenue first.
-- Concepts: WITH (a common table expression): name an intermediate result, then query it.
WITH store_totals AS (
    SELECT store_id,
           SUM(units)       AS units,
           SUM(revenue_sek) AS revenue_sek
    FROM daily_sales
    GROUP BY store_id
)
SELECT c.name AS city,
       t.units,
       ROUND(t.revenue_sek, 2) AS revenue_sek
FROM store_totals AS t
JOIN stores AS s ON s.id = t.store_id
JOIN cities AS c ON c.id = s.city_id
ORDER BY t.revenue_sek DESC;
