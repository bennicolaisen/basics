-- Uppgift 2b: Dagar med regn eller snö, och där högsta temperaturen
-- var under 10 grader. Parentesen gör att OR räknas först.
SELECT id, city_id, observed_on, temp_max_c, conditions
FROM observations
WHERE (conditions = 'rain' OR conditions = 'snow')
  AND temp_max_c < 10;
