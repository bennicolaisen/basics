-- Q06: Each city's daily high next to its three-day moving average (that day and the two before).
-- Concepts: a window frame: ROWS BETWEEN 2 PRECEDING AND CURRENT ROW limits which rows
-- the average covers. The first two days average over fewer rows.
SELECT c.name AS city,
       o.observed_on,
       o.temp_max_c,
       ROUND(AVG(o.temp_max_c) OVER (
           PARTITION BY o.city_id
           ORDER BY o.observed_on
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ), 1) AS three_day_avg_c
FROM observations AS o
JOIN cities AS c ON c.id = o.city_id
ORDER BY c.name, o.observed_on;
