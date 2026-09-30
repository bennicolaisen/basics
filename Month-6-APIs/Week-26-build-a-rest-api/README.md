# Week 26 — APIs II: Building a REST API

## Purpose

Last week you were the client: you sent requests to a server someone else
wrote and dealt with whatever came back. This week you're the server. You
decide which URLs exist, what each method does to them, which status
code each outcome gets, and what happens when a client sends nonsense,
because some client eventually will. The project is a small but complete
REST API for the weather log from Week 22: clients can list and create
cities, and record, read, and delete observations. It's built on
Python's standard library alone, so nothing is hidden: every part a web
framework would normally do for you (reading the request, routing,
turning results into JSON) is written out where you can read it.

## Objectives

The code in this project concretely demonstrates:

- Designing endpoints as resources and methods, and writing the contract
  down before the code.
- Routing a request to a handler by path pattern and method, and the
  difference between `404 Not Found` and `405 Method Not Allowed`.
- Choosing status codes for writes: `201 Created` with a `Location`
  header, `204 No Content`, and `400`, `404` and `409` for the different
  ways a write can fail.
- Validating a JSON request body at the boundary: valid JSON, the right
  shape, no unknown fields, the right types.
- Translating database constraint errors into HTTP errors (a `CHECK` into
  `400`, a `UNIQUE` into `409`).
- Separating what the API decides (`app.py`, a pure function) from moving
  bytes over a socket (`server.py`), so nearly every test runs without a
  network.

## Concepts Refresher

### What a server does

A web server is a loop: wait for a connection, read one request, work
out the answer, write the response, repeat. Python's `http.server`
handles the loop and the parsing of the first line and headers; it calls
a method on your handler class named after the HTTP method (`do_GET`,
`do_POST`, ...) and gives you `self.command`, `self.path` and
`self.headers`. Everything after that is up to you:

1. Read the body, if there is one. HTTP doesn't mark where a body ends,
   so the client sends a `Content-Length` header and the server reads
   exactly that many bytes (`server.py`, `_dispatch`).
2. Route: find which handler, if any, is responsible for this method and
   path.
3. Run the handler: parse and validate input, talk to the database,
   decide the status code.
4. Write the status line, headers, a blank line, and the body.

### The contract first

Before writing any code, write down the API as a client will see it.
Here it is (it's also the docstring at the top of `app.py`):

| Method | Path | Success | Can fail with |
|---|---|---|---|
| GET | `/cities` | 200, list of cities | |
| POST | `/cities` | 201, the city, `Location` header | 400 invalid, 409 name taken |
| GET | `/cities/{name}` | 200, the city | 404 |
| GET | `/cities/{name}/observations?from=&to=` | 200, list | 400 bad date, 404 no such city |
| POST | `/cities/{name}/observations` | 201, the observation, `Location` | 400 invalid, 404 no such city, 409 day already recorded |
| GET | `/cities/{name}/observations/{date}` | 200, the observation | 404 |
| DELETE | `/cities/{name}/observations/{date}` | 204, no body | 404 |

The read endpoints are deliberately the same as Week 25's practice API,
so Week 25's client works against this server unchanged; the writes are
new. A table like
this is the thing clients read, the thing you test against, and the thing
you're not allowed to change casually once people depend on it.

### Routing: 404 or 405?

`ROUTES` in `app.py` is a list of `(path pattern, {method: handler})`
pairs. `handle` tries each pattern with `fullmatch` (the whole path must
match, so `/cities/Oslo/extra` doesn't sneak into the `/cities/{name}`
route). Named groups like `(?P<city>[^/]+)` capture the parts of the path
that vary; `[^/]+` means "one or more characters that aren't a slash", so
a city name can never swallow the rest of the path. Captured values are
percent-decoded with `unquote`, turning `Malm%C3%B6` back into `Malmö`.

Two different failures come out of routing:

- **No pattern matches** → `404 Not Found`: there's no such resource.
- **A pattern matches but not with this method** → `405 Method Not
  Allowed`, plus an `Allow` header listing the methods that do work
  (`Allow: GET, POST`). The resource exists; the client is just asking it
  to do something it doesn't do.

### Status codes for writes

Reads mostly answer `200` or `404`. Writes need more precision, because
the client has to know what happened and what to do next:

- **`201 Created`** for a successful `POST` that made something new. The
  `Location` header gives the new resource's URL, and the body echoes the
  resource as stored, so the client sees exactly what the server kept
  (for example `wind_ms: null` when it wasn't sent).
- **`204 No Content`** for a successful `DELETE`: done, nothing to say.
  A `204` response must not have a body, which is why `server.py` sends
  no `Content-Type` and no `Content-Length` for it.
- **`400 Bad Request`**: the request itself is wrong: not JSON, missing
  fields, wrong types, or values the rules forbid (negative rain, a
  date that doesn't exist). Sending it again won't help.
- **`404 Not Found`**: the resource the request is *about* doesn't exist
  (posting an observation to `/cities/Atlantis/observations`).
- **`409 Conflict`**: the request is fine on its own but clashes with
  the current state: a city with that name already exists, or that day is
  already recorded. It might succeed later (after a delete), and the
  client may want to handle it differently from a typo, for example by
  offering to update the existing record.

Some APIs use **`422 Unprocessable Content`** for "well-formed JSON with
invalid values" and keep `400` for malformed requests. Both conventions
are common; what matters is picking one and documenting it.

### Never trust the request

Anything in a request can be wrong, by accident or on purpose. The rule
from Week 22 applies at the API boundary too: check the *shape* of input
where it arrives, and let the database's constraints decide whether the
*values* are acceptable. `_parse_body` checks, in order:

1. It's valid UTF-8 JSON.
2. It's a JSON object (not a list or a number).
3. It has no unknown fields. Rejecting them catches typos: a client that
   sends `temp_max` instead of `temp_max_c` gets a clear `400` instead of
   having the value silently ignored.
4. Every required field is present, and optional ones get a default
   (`wind_ms` becomes `null`).
5. Each field has the right JSON type. In Python, `True` is an `int`
   (`isinstance(True, int)` is `True`), so booleans are rejected
   explicitly; otherwise `"population": true` would be stored as 1.

What `_parse_body` deliberately doesn't check is whether the values make
sense: that's the schema's job, and the handler turns the database's
refusal into HTTP: `IntegrityError` mentioning `UNIQUE` becomes `409`,
any other `IntegrityError` (a `CHECK`, a `NOT NULL`) becomes `400` with
the constraint in the message. Keeping each rule in one place means the
API and every other program writing to the database can never disagree.

Path parameters are input too. They go into SQL as parameters (`?`),
never pasted into the query text, exactly as in Week 22; a URL is just
another way for a stranger to send you text.

### Idempotency in practice

`DELETE /cities/Visby/observations/2026-09-27` twice: the first call
answers `204`, the second `404`, because there's nothing left to delete.
The *state* after both is the same, which is what idempotent means, so a
client that isn't sure whether its first attempt arrived can safely
retry. `POST` isn't idempotent: retrying a `POST` that did arrive would
try to create a second observation for the same day. Here the database's
`UNIQUE (city_id, observed_on)` turns that into a `409` instead of a
duplicate row, which is exactly the kind of protection you want behind a
non-idempotent method.

### Stateless requests

Each request carries everything the server needs to answer it: the
method, the full path, the body. The server doesn't remember anything
about a client between requests (all the remembering happens in the
database). That's what lets a real API run on many servers at once,
since any of them can answer any request, and it's why a client can
retry against the same URL without a "session" to restore.

### Pure logic, thin I/O

`app.handle(conn, method, target, body)` returns a `Response(status,
body, headers)` and never touches a socket. `server.py` reads bytes off
the connection, calls `handle`, and writes the result back. That split
is the same one every earlier week made between logic and the terminal
or filesystem, and it pays off the same way: `test_app.py` checks every
rule of the API by calling a function, fast and without a network, and
only `test_server.py` needs a real server, to check the part that
actually does HTTP.

### What a framework would do for you

Frameworks like Flask and FastAPI replace `ROUTES`, `_parse_body` and
`server.py` with decorators and declared models:

```python
@app.post("/cities/{name}/observations", status_code=201)
def create_observation(name: str, observation: Observation): ...
```

They also bring what `http.server` lacks for production use: handling
many requests at once, HTTPS, authentication, logging, and generated
documentation. `http.server` is fine for learning and for tools on your
own machine, and Python's documentation says plainly not to use it for
production. Once you've written the pieces by hand, a framework is much
less magical: it's doing what this week's code does.

## Design & Architecture

```
Week-26-build-a-rest-api/
├── conftest.py                  - adds src/ to sys.path for pytest
├── src/
│   └── weather_api/
│       ├── __init__.py
│       ├── schema.sql           - Week 22's schema: the data rules
│       ├── store.py             - all SQL; knows nothing about HTTP
│       ├── app.py               - routes, validation, status codes: handle() -> Response
│       ├── server.py            - http.server adapter and the command line
│       └── data/
│           └── sample_data.sql  - the sample week from Weeks 19-22
└── tests/
    ├── test_app.py              - every endpoint and error, by calling handle() directly
    └── test_server.py           - the same API over real HTTP, checking the byte-level details
```

Three layers, each ignorant of the one above it. `store.py` speaks SQL
and returns rows. `app.py` speaks HTTP concepts (methods, paths, status
codes, JSON) and calls `store.py`. `server.py` speaks sockets and calls
`app.handle`. You could replace `server.py` with a framework, or
`store.py` with a different database, without touching the other two.

## How to Build & Run

```bash
cd Month-6-APIs/Week-26-build-a-rest-api
export PYTHONPATH=src            # PowerShell: $env:PYTHONPATH="src"

# Terminal 1: start the API on a database file, with the sample week loaded:
python3 -m weather_api.server weather.db --sample
```

In a second terminal, try every kind of response with `curl` (`-i` shows
the status line and headers):

```bash
curl -i http://127.0.0.1:8000/cities/Kiruna
curl -i -X POST http://127.0.0.1:8000/cities \
     -d '{"name": "Bergen", "country": "Norway", "population": 291940}'
curl -i -X POST http://127.0.0.1:8000/cities/Bergen/observations \
     -d '{"observed_on": "2026-09-28", "temp_max_c": 11.5, "temp_min_c": 7.0, "precipitation_mm": 14.2, "conditions": "rain"}'
curl -i -X POST http://127.0.0.1:8000/cities/Bergen/observations \
     -d '{"observed_on": "2026-09-28", "temp_max_c": 11.5, "temp_min_c": 7.0, "precipitation_mm": 14.2, "conditions": "rain"}'   # 409
curl -i -X DELETE http://127.0.0.1:8000/cities/Bergen/observations/2026-09-28
curl -i -X PUT http://127.0.0.1:8000/cities/Bergen                                          # 405
```

(In Windows PowerShell, `curl` may be an alias for `Invoke-WebRequest`:
type `curl.exe` instead, and put the JSON in a file and pass
`-d "@body.json"` to avoid quoting trouble.) Week 25's client works against this API too: run its `cities`
or `observations` commands while this server is running on port 8000.
Because the data is in `weather.db`, what you create survives restarting
the server; delete the file to start over.

## Testing

```bash
cd Month-6-APIs/Week-26-build-a-rest-api
python3 -m pytest -q
```

`test_app.py` exercises the API through `handle()`: every read (including
an encoded city name, an empty list for a city without observations, and
a `null` wind reading), creating cities (`201` with an encoded
`Location`, `409` for a taken name, a `CHECK` turned into `400`, and six
malformed bodies, among them the `true`-is-an-int trap and an unknown
field), recording observations (optional wind, integers accepted as
numbers, `404` for an unknown city, `409` for a recorded day, four values
the schema rejects, and nothing stored on refusal), deleting (`204`, then
`404`), and routing (unknown paths, extra path parts, and `405` with the
right `Allow` header). `test_server.py` runs the API over real HTTP and
checks what only the server layer can get wrong: the `Content-Type` and
`Content-Length` headers, reading a `POST` body, JSON error bodies, and a
`204` with no body and no content type.

## Try It Yourself

1. Add `PATCH /cities/{name}/observations/{date}`, which accepts a JSON
   object with any subset of the observation's fields (except
   `observed_on`) and updates only those. Decide which status codes it
   returns, add them to the contract table, and write the tests first.
2. Add `DELETE /cities/{name}`. What should happen to the city's
   observations? The schema already decides (look for `ON DELETE`); make
   sure the API's behavior and its documentation say the same thing.
3. Add `GET /cities/{name}/summary`, returning the number of
   observations, the average high, and the total precipitation, computed
   in SQL (Week 20). Then add `?from=` and `?to=` to it.
4. Protect the write endpoints with an API key: a request must send the
   header `X-API-Key` with a value the server reads from an environment
   variable at startup, or get `401`. Reads stay open. Where in the three
   layers does this check belong, and why?
5. Extend Week 25's `WeatherClient` with `add_observation(city,
   observation)` that `POST`s to this API and returns the stored
   observation, raising `ApiError` with the status on `400`, `404` and
   `409`. Test it against this week's server.

## Reflection

**Why the handlers look boring.** Each handler is a few lines: parse,
call `store`, pick a status. The interesting decisions (which status for
which failure, what counts as invalid) were made in the contract table
and in the schema, before the code. That's usually a sign of a well-
designed API: the code is the least surprising part.

**Versioning.** Once other people's programs depend on your API,
renaming a field or changing a status code breaks them. Real APIs deal
with that by putting a version in the path (`/v1/cities`) and only making
breaking changes in a new version. This project doesn't, because it has
no users yet; it's the first thing to add when it does.
