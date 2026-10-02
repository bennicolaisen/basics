-- Uppgift 5: Medelvind per stad om saknade värden räknas som 0, bredvid
-- det korrekta medelvärdet från q08 (som bara räknar kända värden).
SELECT city_id,
       ROUND(AVG(COALESCE(wind_ms, 0)), 2) AS avg_wind_missing_as_zero,
       ROUND(AVG(wind_ms), 2)              AS avg_wind_known_only
FROM observations
GROUP BY city_id
ORDER BY city_id;
