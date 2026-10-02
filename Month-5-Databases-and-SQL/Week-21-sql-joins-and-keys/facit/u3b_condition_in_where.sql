-- Uppgift 3b: Villkoret i WHERE. WHERE körs efter joinen och tar bort
-- raderna där o.conditions är NULL, så LEFT JOIN beter sig som JOIN.
SELECT c.name, o.observed_on
FROM cities c
LEFT JOIN observations o ON o.city_id = c.id
WHERE o.conditions = 'snow';
