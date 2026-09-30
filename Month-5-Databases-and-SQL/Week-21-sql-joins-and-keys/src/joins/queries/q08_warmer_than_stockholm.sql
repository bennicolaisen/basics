-- Q08: On each day, which cities had a higher high than Stockholm?
-- Concepts: joining a table to itself, with two aliases for two different roles.
SELECT o.observed_on,
       c.name,
       o.temp_max_c,
       sthlm.temp_max_c AS stockholm_max_c
FROM observations AS o
JOIN cities AS c ON c.id = o.city_id
JOIN observations AS sthlm ON sthlm.observed_on = o.observed_on
JOIN cities AS sthlm_city ON sthlm_city.id = sthlm.city_id
WHERE sthlm_city.name = 'Stockholm'
  AND o.temp_max_c > sthlm.temp_max_c
ORDER BY o.observed_on, c.name;
