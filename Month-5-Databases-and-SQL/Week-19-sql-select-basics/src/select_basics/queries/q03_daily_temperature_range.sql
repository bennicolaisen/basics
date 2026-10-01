-- Q03: For every observation, how far apart were the day's high and low?
-- Concepts: computed columns, ROUND, naming a result column with AS.
SELECT observed_on,
       city_id,
       ROUND(temp_max_c - temp_min_c, 1) AS range_c
FROM observations;
