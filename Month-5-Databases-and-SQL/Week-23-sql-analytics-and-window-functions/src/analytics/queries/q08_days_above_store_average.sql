-- Q08: Days on which a store beat its own average daily revenue for the week.
-- Concepts: a window function can't be used in WHERE (it's computed after WHERE),
-- so compute it in a CTE and filter in the outer query.
WITH daily AS (
    SELECT store_id, sold_on, SUM(revenue_sek) AS revenue_sek
    FROM daily_sales
    GROUP BY store_id, sold_on
),
with_average AS (
    SELECT store_id,
           sold_on,
           revenue_sek,
           AVG(revenue_sek) OVER (PARTITION BY store_id) AS store_avg_sek
    FROM daily
)
SELECT c.name AS city,
       w.sold_on,
       ROUND(w.revenue_sek, 2)   AS revenue_sek,
       ROUND(w.store_avg_sek, 2) AS store_avg_sek
FROM with_average AS w
JOIN stores AS s ON s.id = w.store_id
JOIN cities AS c ON c.id = s.city_id
WHERE w.revenue_sek > w.store_avg_sek
ORDER BY c.name, w.sold_on;
