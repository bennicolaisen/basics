-- Q09: For each country, how many cities are in the table and how many people live in them?
-- Concepts: GROUP BY on a text column; SUM of an INTEGER column stays an integer.
SELECT country,
       COUNT(*)        AS cities,
       SUM(population) AS population
FROM cities
GROUP BY country
ORDER BY population DESC;
