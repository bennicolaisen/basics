-- Q06: Which days had frost overnight (low below zero) or wind above 10 m/s?
-- Concepts: OR (either condition is enough).
SELECT observed_on, city_id, temp_min_c, wind_ms
FROM observations
WHERE temp_min_c < 0
   OR wind_ms > 10;
