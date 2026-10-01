-- Q04: How many days of each kind of weather were there? Most common first.
-- Concepts: GROUP BY, one result row per group, ORDER BY an aggregate's alias.
SELECT conditions,
       COUNT(*) AS days
FROM observations
GROUP BY conditions
ORDER BY days DESC, conditions;
