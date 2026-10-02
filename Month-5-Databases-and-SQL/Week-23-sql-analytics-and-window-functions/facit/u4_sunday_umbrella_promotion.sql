-- Uppgift 4: Söndagens paraplyförsäljning (kampanjdagen) i varje butik,
-- jämförd med butikens snitt övriga dagar och med snittet övriga dagar
-- som hade SAMMA väder som söndagen. Dagar utan sålda paraplyer räknas
-- som 0, som i q07.
WITH store_days AS (
    SELECT s.id AS store_id, s.city_id, o.observed_on, o.conditions
    FROM stores AS s
    JOIN observations AS o ON o.city_id = s.city_id
),
umbrella_sales AS (
    SELECT ds.store_id, ds.sold_on, ds.units
    FROM daily_sales AS ds
    JOIN products AS p ON p.id = ds.product_id
    WHERE p.name = 'Umbrella'
),
per_day AS (
    SELECT sd.store_id, sd.city_id, sd.observed_on, sd.conditions,
           COALESCE(u.units, 0) AS units
    FROM store_days AS sd
    LEFT JOIN umbrella_sales AS u
           ON u.store_id = sd.store_id AND u.sold_on = sd.observed_on
),
sunday AS (
    SELECT store_id, conditions AS sunday_weather, units AS sunday_units
    FROM per_day
    WHERE observed_on = '2026-09-27'
)
SELECT c.name AS city,
       su.sunday_weather,
       su.sunday_units,
       ROUND(AVG(d.units), 2) AS other_days_avg_units,
       ROUND(AVG(CASE WHEN d.conditions = su.sunday_weather THEN d.units END), 2)
           AS same_weather_days_avg_units,
       COUNT(CASE WHEN d.conditions = su.sunday_weather THEN 1 END)
           AS same_weather_days
FROM sunday AS su
JOIN per_day AS d ON d.store_id = su.store_id AND d.observed_on <> '2026-09-27'
JOIN cities  AS c ON c.id = d.city_id
GROUP BY su.store_id, c.name, su.sunday_weather, su.sunday_units
ORDER BY c.name;
