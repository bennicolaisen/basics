-- Uppgift 2: Butiksdagar där intäkten ökade två dagar i rad: högre än
-- dagen innan, som i sin tur var högre än dagen före den.
WITH daily AS (
    SELECT store_id, sold_on, SUM(revenue_sek) AS revenue_sek
    FROM daily_sales
    GROUP BY store_id, sold_on
),
with_history AS (
    SELECT store_id,
           sold_on,
           revenue_sek,
           LAG(revenue_sek, 1) OVER by_day AS one_day_before,
           LAG(revenue_sek, 2) OVER by_day AS two_days_before
    FROM daily
    WINDOW by_day AS (PARTITION BY store_id ORDER BY sold_on)
)
SELECT c.name AS city,
       h.sold_on,
       ROUND(h.two_days_before, 2) AS two_days_before_sek,
       ROUND(h.one_day_before, 2)  AS one_day_before_sek,
       ROUND(h.revenue_sek, 2)     AS revenue_sek
FROM with_history AS h
JOIN stores AS s ON s.id = h.store_id
JOIN cities AS c ON c.id = s.city_id
WHERE h.two_days_before < h.one_day_before
  AND h.one_day_before < h.revenue_sek
ORDER BY c.name, h.sold_on;
