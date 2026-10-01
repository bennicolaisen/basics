-- Q02: What were the week's coldest low, warmest high, and average high?
-- Concepts: MIN, MAX, AVG; several aggregates in one query give one row.
SELECT MIN(temp_min_c)           AS coldest_low_c,
       MAX(temp_max_c)           AS warmest_high_c,
       ROUND(AVG(temp_max_c), 1) AS average_high_c
FROM observations;
