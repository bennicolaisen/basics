-- Uppgift 3, jämförelse: samma gräns i WHERE. Raderna under 13 grader
-- tas bort FÖRE grupperingen, så MIN räknas bara på de varma dagarna, och
-- Stockholm och Oslo kommer felaktigt med.
SELECT city_id,
       MIN(temp_max_c) AS lowest_high_c
FROM observations
WHERE temp_max_c > 13
GROUP BY city_id
ORDER BY city_id;
