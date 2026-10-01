-- Q11: Which kinds of weather occur at all? Each kind once, alphabetically.
-- Concepts: DISTINCT removes duplicate result rows.
SELECT DISTINCT conditions
FROM observations
ORDER BY conditions;
