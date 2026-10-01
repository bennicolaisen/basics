-- Q03: How much precipitation fell in total, across every city and day?
-- Concepts: SUM.
SELECT ROUND(SUM(precipitation_mm), 1) AS total_mm
FROM observations;
