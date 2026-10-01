-- Q04: Which observations recorded more than 5 mm of precipitation?
-- Concepts: WHERE with a numeric comparison.
SELECT *
FROM observations
WHERE precipitation_mm > 5;
