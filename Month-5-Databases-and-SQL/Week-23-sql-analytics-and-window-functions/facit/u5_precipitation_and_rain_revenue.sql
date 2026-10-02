-- Uppgift 5: Nederbörd från observations och intäkt för regnprodukter från
-- daily_sales, sida vid sida, en rad per stad.
--
-- Varje tabell summeras för sig i en egen CTE, till EN rad per stad, och
-- först därefter joinas resultaten. Då kan ingen rad dupliceras (fan-out).
WITH precipitation AS (
    SELECT city_id, ROUND(SUM(precipitation_mm), 1) AS precipitation_mm
    FROM observations
    GROUP BY city_id
),
rain_revenue AS (
    SELECT s.city_id, ROUND(SUM(ds.revenue_sek), 2) AS rain_revenue_sek
    FROM daily_sales AS ds
    JOIN products AS p ON p.id = ds.product_id
    JOIN stores   AS s ON s.id = ds.store_id
    WHERE p.category = 'rain'
    GROUP BY s.city_id
)
SELECT c.name AS city,
       pr.precipitation_mm,
       COALESCE(rr.rain_revenue_sek, 0) AS rain_revenue_sek
FROM cities AS c
JOIN precipitation     AS pr ON pr.city_id = c.id
LEFT JOIN rain_revenue AS rr ON rr.city_id = c.id
ORDER BY c.name;
