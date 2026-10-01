-- Q04: Stockholm's revenue day by day, with a running total for the week so far.
-- Concepts: SUM(...) OVER (ORDER BY ...) is a running total: each row sums itself
-- and every row before it in the window's order.
WITH daily AS (
    SELECT sold_on, SUM(revenue_sek) AS revenue_sek
    FROM daily_sales
    WHERE store_id = (SELECT s.id FROM stores AS s JOIN cities AS c ON c.id = s.city_id
                      WHERE c.name = 'Stockholm')
    GROUP BY sold_on
)
SELECT sold_on,
       ROUND(revenue_sek, 2) AS revenue_sek,
       ROUND(SUM(revenue_sek) OVER (ORDER BY sold_on), 2) AS week_to_date_sek
FROM daily
ORDER BY sold_on;
