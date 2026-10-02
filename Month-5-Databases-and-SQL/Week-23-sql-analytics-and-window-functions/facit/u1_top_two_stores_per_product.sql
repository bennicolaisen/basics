-- Uppgift 1: För varje produkt, ranka butikerna efter sålda enheter med
-- DENSE_RANK och visa bara varje produkts två bästa placeringar.
WITH units_per_store AS (
    SELECT product_id, store_id, SUM(units) AS units
    FROM daily_sales
    GROUP BY product_id, store_id
),
ranked AS (
    SELECT product_id,
           store_id,
           units,
           DENSE_RANK() OVER (PARTITION BY product_id ORDER BY units DESC) AS units_rank
    FROM units_per_store
)
SELECT p.name AS product,
       c.name AS city,
       r.units,
       r.units_rank
FROM ranked AS r
JOIN products AS p ON p.id = r.product_id
JOIN stores   AS s ON s.id = r.store_id
JOIN cities   AS c ON c.id = s.city_id
WHERE r.units_rank <= 2
ORDER BY p.id, r.units_rank, c.name;
