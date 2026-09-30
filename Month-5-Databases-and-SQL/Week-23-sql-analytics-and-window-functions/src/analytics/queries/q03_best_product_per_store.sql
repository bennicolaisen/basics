-- Q03: Each store's best-selling product by revenue.
-- Concepts: ROW_NUMBER() OVER (PARTITION BY ...) numbers rows within each group;
-- keeping row 1 per group is the standard "top-1 per group" pattern.
WITH product_totals AS (
    SELECT store_id, product_id, SUM(revenue_sek) AS revenue_sek
    FROM daily_sales
    GROUP BY store_id, product_id
),
ranked AS (
    SELECT store_id,
           product_id,
           revenue_sek,
           ROW_NUMBER() OVER (PARTITION BY store_id ORDER BY revenue_sek DESC) AS position
    FROM product_totals
)
SELECT c.name AS city,
       p.name AS product,
       ROUND(r.revenue_sek, 2) AS revenue_sek
FROM ranked AS r
JOIN stores AS s ON s.id = r.store_id
JOIN cities AS c ON c.id = s.city_id
JOIN products AS p ON p.id = r.product_id
WHERE r.position = 1
ORDER BY c.name;
