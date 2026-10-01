-- Q01: How many observations are there, and how many of them have a wind reading?
-- Concepts: COUNT(*) counts rows; COUNT(column) counts non-NULL values.
SELECT COUNT(*)       AS observations,
       COUNT(wind_ms) AS wind_readings
FROM observations;
