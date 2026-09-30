-- Q11: How many frost nights (low below zero) did each city have? Include cities with none.
-- Concepts: CASE inside SUM ("conditional aggregation") counts only matching rows per group.
SELECT city_id,
       SUM(CASE WHEN temp_min_c < 0 THEN 1 ELSE 0 END) AS frost_nights
FROM observations
GROUP BY city_id
ORDER BY frost_nights DESC, city_id;
