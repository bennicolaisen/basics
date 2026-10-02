-- Uppgift 3a: Villkoret i ON. Alla städer behålls; de utan snö får NULL.
SELECT c.name, o.observed_on
FROM cities c
LEFT JOIN observations o ON o.city_id = c.id AND o.conditions = 'snow';
