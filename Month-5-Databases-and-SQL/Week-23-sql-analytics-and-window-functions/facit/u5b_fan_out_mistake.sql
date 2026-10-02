-- Uppgift 5, jämförelse: det FELAKTIGA sättet. Joina först och summera
-- sedan. Varje observation paras ihop med varje försäljningsrad samma
-- stad (för regnprodukter), så nederbörden räknas många gånger.
SELECT c.name AS city,
       ROUND(SUM(o.precipitation_mm), 1) AS precipitation_mm,
       ROUND(SUM(ds.revenue_sek), 2)     AS rain_revenue_sek
FROM cities AS c
JOIN observations AS o  ON o.city_id = c.id
JOIN stores       AS s  ON s.city_id = c.id
JOIN daily_sales  AS ds ON ds.store_id = s.id
JOIN products     AS p  ON p.id = ds.product_id AND p.category = 'rain'
GROUP BY c.id, c.name
ORDER BY c.name;
