-- The weather API's schema: Week 22's weather log, unchanged.
--
-- Every rule about valid data lives here, so the API can hand bad values
-- to the database and turn its refusal into a 400 or 409 response.
--
-- IF NOT EXISTS makes this script safe to run every time a log is opened:
-- it creates the tables in a new file and does nothing in an existing one.

CREATE TABLE IF NOT EXISTS cities (
    id          INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL UNIQUE,
    country     TEXT    NOT NULL,
    population  INTEGER NOT NULL CHECK (population >= 0)
);

CREATE TABLE IF NOT EXISTS observations (
    id                INTEGER PRIMARY KEY,
    city_id           INTEGER NOT NULL REFERENCES cities (id) ON DELETE CASCADE,
    -- date() returns NULL for text it can't parse, and a CHECK whose result
    -- is NULL passes, so compare with IS (NULL-safe) rather than =.
    observed_on       TEXT    NOT NULL CHECK (date(observed_on) IS observed_on),
    temp_max_c        REAL    NOT NULL,
    temp_min_c        REAL    NOT NULL,
    precipitation_mm  REAL    NOT NULL CHECK (precipitation_mm >= 0),
    wind_ms           REAL             CHECK (wind_ms >= 0),
    conditions        TEXT    NOT NULL CHECK (conditions IN ('sun', 'cloud', 'rain', 'snow')),
    CHECK (temp_min_c <= temp_max_c),
    UNIQUE (city_id, observed_on)
);
