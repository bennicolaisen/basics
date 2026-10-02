-- Uppgift 3: Varje butiks intäkt per 1 000 invånare i staden, rankad,
-- bredvid rankningen på total intäkt från q02.
WITH store_totals AS (
    SELECT store_id, SUM(revenue_sek) AS revenue_sek
    FROM daily_sales
    GROUP BY store_id
)
SELECT c.name AS city,
       c.population,
       ROUND(t.revenue_sek, 2)                        AS revenue_sek,
       ROUND(1000.0 * t.revenue_sek / c.population, 2) AS revenue_per_1000_inhabitants,
       RANK() OVER (ORDER BY t.revenue_sek / c.population DESC) AS per_inhabitant_rank,
       RANK() OVER (ORDER BY t.revenue_sek DESC)                AS total_revenue_rank
FROM store_totals AS t
JOIN stores AS s ON s.id = t.store_id
JOIN cities AS c ON c.id = s.city_id
ORDER BY per_inhabitant_rank;
