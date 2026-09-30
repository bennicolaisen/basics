-- Q08: Each city's average wind speed, windiest first, with how many readings it's based on.
-- Concepts: AVG ignores NULL, so it averages over the known readings only.
SELECT city_id,
       COUNT(*)                AS days,
       COUNT(wind_ms)          AS wind_readings,
       ROUND(AVG(wind_ms), 2)  AS average_wind_ms
FROM observations
GROUP BY city_id
ORDER BY average_wind_ms DESC;
