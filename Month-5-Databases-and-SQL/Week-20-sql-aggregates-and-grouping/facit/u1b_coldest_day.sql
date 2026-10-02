-- Uppgift 1, följdfråga: vilken dag var kallast i genomsnitt?
SELECT observed_on,
       ROUND(AVG(temp_max_c), 1) AS avg_high_c
FROM observations
GROUP BY observed_on
ORDER BY AVG(temp_max_c)
LIMIT 1;
