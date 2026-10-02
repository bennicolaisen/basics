-- Uppgift 2: Torra dagar (0 mm) och blöta dagar (mer än 0 mm) per stad,
-- sida vid sida. Varje CASE ger 1 för dagar som räknas och 0 annars, och
-- SUM räknar ihop ettorna.
SELECT city_id,
       SUM(CASE WHEN precipitation_mm = 0 THEN 1 ELSE 0 END) AS dry_days,
       SUM(CASE WHEN precipitation_mm > 0 THEN 1 ELSE 0 END) AS wet_days
FROM observations
GROUP BY city_id
ORDER BY city_id;
