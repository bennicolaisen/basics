-- Facit vecka 22: veckans schema efter uppgift 3 och 4.
--
-- Uppgift 3: observations har inte längre ON DELETE CASCADE. En stad med
-- observationer kan därför inte tas bort förrän observationerna är borta.
-- Uppgift 4: en ny tabell, warnings, med egna CHECK-regler.

CREATE TABLE IF NOT EXISTS cities (
    id          INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL UNIQUE,
    country     TEXT    NOT NULL,
    population  INTEGER NOT NULL CHECK (population >= 0)
);

CREATE TABLE IF NOT EXISTS observations (
    id                INTEGER PRIMARY KEY,
    city_id           INTEGER NOT NULL REFERENCES cities (id),
    observed_on       TEXT    NOT NULL CHECK (date(observed_on) IS observed_on),
    temp_max_c        REAL    NOT NULL,
    temp_min_c        REAL    NOT NULL,
    precipitation_mm  REAL    NOT NULL CHECK (precipitation_mm >= 0),
    wind_ms           REAL             CHECK (wind_ms >= 0),
    conditions        TEXT    NOT NULL CHECK (conditions IN ('sun', 'cloud', 'rain', 'snow')),
    CHECK (temp_min_c <= temp_max_c),
    UNIQUE (city_id, observed_on)
);

CREATE TABLE IF NOT EXISTS warnings (
    id         INTEGER PRIMARY KEY,
    city_id    INTEGER NOT NULL REFERENCES cities (id),
    level      TEXT    NOT NULL CHECK (level IN ('yellow', 'orange', 'red')),
    message    TEXT    NOT NULL CHECK (trim(message) <> ''),
    starts_on  TEXT    NOT NULL CHECK (date(starts_on) IS starts_on),
    ends_on    TEXT    NOT NULL CHECK (date(ends_on) IS ends_on),
    CHECK (starts_on <= ends_on)
);
