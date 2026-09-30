-- Q09: Revenue per store split into the three product categories, one row per store.
-- Concepts: pivoting rows into columns with SUM(CASE ...) (conditional aggregation).
SELECT c.name AS city,
       ROUND(SUM(CASE WHEN p.category = 'rain' THEN ds.revenue_sek ELSE 0 END), 2) AS rain_sek,
       ROUND(SUM(CASE WHEN p.category = 'cold' THEN ds.revenue_sek ELSE 0 END), 2) AS cold_sek,
       ROUND(SUM(CASE WHEN p.category = 'sun'  THEN ds.revenue_sek ELSE 0 END), 2) AS sun_sek
FROM daily_sales AS ds
JOIN products AS p ON p.id = ds.product_id
JOIN stores AS s ON s.id = ds.store_id
JOIN cities AS c ON c.id = s.city_id
GROUP BY c.name
ORDER BY c.name;
