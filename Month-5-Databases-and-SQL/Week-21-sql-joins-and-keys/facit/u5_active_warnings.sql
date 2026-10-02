-- Uppgift 5: Vädervarningar. En varning gäller en stad, har en nivå och
-- en text, och gäller från ett datum till och med ett annat.

CREATE TABLE warnings (
    id         INTEGER PRIMARY KEY,
    city_id    INTEGER NOT NULL REFERENCES cities (id),
    level      TEXT    NOT NULL CHECK (level IN ('yellow', 'orange', 'red')),
    message    TEXT    NOT NULL,
    starts_on  TEXT    NOT NULL,  -- 'YYYY-MM-DD', första dagen
    ends_on    TEXT    NOT NULL,  -- 'YYYY-MM-DD', sista dagen (ingår)
    CHECK (starts_on <= ends_on)
);

INSERT INTO warnings (id, city_id, level, message, starts_on, ends_on) VALUES
    (1, 2, 'orange', 'Heavy rain, risk of flooding', '2026-09-22', '2026-09-23'),
    (2, 6, 'yellow', 'Strong wind',                  '2026-09-23', '2026-09-24'),
    (3, 5, 'yellow', 'Snow and slippery roads',      '2026-09-23', '2026-09-24'),
    (4, 7, 'yellow', 'Heavy rain',                   '2026-09-24', '2026-09-24'),
    (5, 1, 'yellow', 'Strong wind',                  '2026-09-20', '2026-09-22');

-- Städer med en aktiv varning den 23 september.
SELECT c.name, w.level, w.message
FROM warnings w
JOIN cities c ON c.id = w.city_id
WHERE '2026-09-23' BETWEEN w.starts_on AND w.ends_on
ORDER BY c.name;
