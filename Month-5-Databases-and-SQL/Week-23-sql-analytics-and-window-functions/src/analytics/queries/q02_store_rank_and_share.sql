-- Q02: Rank the stores by revenue and show each store's share of the chain's total.
-- Concepts: window functions: RANK() OVER (...) and SUM(...) OVER () keep every row
-- while computing across rows, unlike GROUP BY which collapses them.
WITH store_totals AS (
    SELECT store_id, SUM(revenue_sek) AS revenue_sek
    FROM daily_sales
    GROUP BY store_id
)
SELECT c.name AS city,
       ROUND(t.revenue_sek, 2) AS revenue_sek,
       RANK() OVER (ORDER BY t.revenue_sek DESC) AS revenue_rank,
       ROUND(100.0 * t.revenue_sek / SUM(t.revenue_sek) OVER (), 1) AS share_pct
FROM store_totals AS t
JOIN stores AS s ON s.id = t.store_id
JOIN cities AS c ON c.id = s.city_id
ORDER BY revenue_rank;
