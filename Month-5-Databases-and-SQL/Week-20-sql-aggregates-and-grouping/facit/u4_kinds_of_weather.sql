-- Uppgift 4: Hur många olika sorters väder varje stad hade, bara städer
-- med tre eller fler.
SELECT city_id,
       COUNT(DISTINCT conditions) AS kinds_of_weather
FROM observations
GROUP BY city_id
HAVING COUNT(DISTINCT conditions) >= 3
ORDER BY city_id;
