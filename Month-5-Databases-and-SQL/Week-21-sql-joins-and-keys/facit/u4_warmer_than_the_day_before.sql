-- Uppgift 4: Observationer där dagens högsta var minst 2 grader varmare
-- än samma stads högsta dagen innan. Tabellen joinas med sig själv: en
-- gång som "today" och en gång som "yesterday".
SELECT c.name,
       today.observed_on,
       yesterday.temp_max_c                                AS high_day_before_c,
       today.temp_max_c                                    AS high_c,
       ROUND(today.temp_max_c - yesterday.temp_max_c, 1)   AS rise_c
FROM observations today
JOIN observations yesterday
  ON yesterday.city_id = today.city_id
 AND yesterday.observed_on = date(today.observed_on, '-1 day')
JOIN cities c ON c.id = today.city_id
WHERE ROUND(today.temp_max_c - yesterday.temp_max_c, 1) >= 2
ORDER BY today.observed_on, c.name;
