-- Q07: Do umbrellas sell better when it rains? Average umbrella units per store-day,
-- on rainy days versus all other days.
-- Concepts: building the full set of store-days first, then LEFT JOIN-ing sales so days
-- with no umbrella sales count as 0 instead of silently disappearing from the average.
WITH store_days AS (
    SELECT s.id AS store_id, o.observed_on, o.conditions
    FROM stores AS s
    JOIN observations AS o ON o.city_id = s.city_id
),
umbrella_sales AS (
    SELECT ds.store_id, ds.sold_on, ds.units
    FROM daily_sales AS ds
    JOIN products AS p ON p.id = ds.product_id
    WHERE p.name = 'Umbrella'
)
SELECT CASE WHEN sd.conditions = 'rain' THEN 'rain' ELSE 'no rain' END AS weather,
       COUNT(*)                            AS store_days,
       ROUND(AVG(COALESCE(u.units, 0)), 2) AS avg_umbrellas_per_day
FROM store_days AS sd
LEFT JOIN umbrella_sales AS u
       ON u.store_id = sd.store_id AND u.sold_on = sd.observed_on
GROUP BY weather
ORDER BY weather DESC;
