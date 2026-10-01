-- Q08: Show the rows for the three capitals: Stockholm, Oslo and Copenhagen.
-- Concepts: IN, a shorthand for several ORs on the same column.
SELECT name, country, population
FROM cities
WHERE name IN ('Stockholm', 'Oslo', 'Copenhagen');
