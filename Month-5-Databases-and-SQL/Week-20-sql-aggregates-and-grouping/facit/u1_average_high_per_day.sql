-- Uppgift 1: Medeltemperaturen (dagens högsta) över alla städer, och hur
-- många städer som rapporterade, per datum i datumordning.
SELECT observed_on,
       ROUND(AVG(temp_max_c), 1) AS avg_high_c,
       COUNT(*)                  AS cities_reporting
FROM observations
GROUP BY observed_on
ORDER BY observed_on;
