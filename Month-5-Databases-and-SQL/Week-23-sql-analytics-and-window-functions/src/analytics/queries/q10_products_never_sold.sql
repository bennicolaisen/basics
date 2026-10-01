-- Q10: Which products did each store not sell at all this week?
-- Concepts: every (store, product) pair from a join with no ON condition to speak of
-- (a cross join), filtered with NOT EXISTS and a correlated subquery.
SELECT c.name AS city,
       p.name AS product
FROM stores AS s
JOIN cities AS c ON c.id = s.city_id
CROSS JOIN products AS p
WHERE NOT EXISTS (
    SELECT 1
    FROM daily_sales AS ds
    WHERE ds.store_id = s.id
      AND ds.product_id = p.id
)
ORDER BY c.name, p.name;
