-- Q05: For every store and day, the revenue and how much it changed from the day before.
-- Concepts: LAG(...) OVER (PARTITION BY ... ORDER BY ...) reads a value from the previous
-- row in the same partition; it's NULL on the first row, where there's no previous day.
WITH daily AS (
    SELECT store_id, sold_on, SUM(revenue_sek) AS revenue_sek
    FROM daily_sales
    GROUP BY store_id, sold_on
)
SELECT c.name AS city,
       d.sold_on,
       ROUND(d.revenue_sek, 2) AS revenue_sek,
       ROUND(d.revenue_sek - LAG(d.revenue_sek) OVER (PARTITION BY d.store_id ORDER BY d.sold_on), 2)
           AS change_sek
FROM daily AS d
JOIN stores AS s ON s.id = d.store_id
JOIN cities AS c ON c.id = s.city_id
ORDER BY c.name, d.sold_on;
