# Week 25 — APIs I: HTTP, JSON, and Calling an API

## Purpose

A weather app doesn't measure the weather. It asks another program, run
by someone else on another computer, and gets the answer back as data.
That other program's **API** (application programming interface) is the
set of requests it promises to understand and the answers it promises to
give. Almost every modern application is built this way: the phone app
talks to its server's API, the server talks to a payment provider's API,
and so on. This week is about the client side: what actually travels over
the network when a program calls a web API, how to read the answer, and
how to handle the ways it can go wrong. You'll practise against a small
weather API that runs on your own machine, and then call a real public
one. Week 26 turns it around and has you build the server.

## Objectives

The code in this project concretely demonstrates:

- What an HTTP request and response contain: method, URL, headers, body,
  status code. The `raw` command prints a real exchange.
- The parts of a URL, and percent-encoding for values like `Malmö`.
- JSON as the data format, and how its types map onto Python's.
- Resource-style (REST) endpoints: collections, items, and query
  parameters for filtering.
- Reading status codes, and telling apart "the server said no" (an
  `ApiError` with a status) from "no server answered" (`ConnectionError`).
- Wrapping an API in a small client class, so the rest of a program never
  deals with URLs or status codes.
- Calling a real public API (Open-Meteo) and reshaping its
  column-oriented JSON into one record per day.

## Concepts Refresher

### An API is a contract

Calling a function in your own program is easy: you know its name, its
parameters, and what it returns. An API is the same idea across a
network. The provider publishes a contract ("send a GET request to
`/cities/{name}` and you'll get the city as JSON, or a 404 if there's no
such city") and anyone can write a program against it without seeing the
provider's code, knowing its programming language, or caring what
database it uses. The practice API in this project is written in Python
over SQLite, but your client only ever sees the contract listed at the top
of `practice_api.py`.

The program that asks is the **client**; the one that answers is the
**server**. The client always speaks first, and every exchange is one
**request** and one **response**.

### Anatomy of a URL

```
http://127.0.0.1:8000/cities/Kiruna/observations?from=2026-09-23&to=2026-09-25
└┬─┘   └───┬───┘ └┬─┘└──────────┬─────────────┘ └──────────┬──────────────┘
scheme    host   port          path                    query string
```

- **Scheme**: `http`, or `https` for an encrypted connection. Real APIs
  use `https`; the local practice API uses `http` because nothing leaves
  your machine.
- **Host** and **port**: which computer, and which program on it.
  `127.0.0.1` (also called `localhost`) is always "this computer".
- **Path**: which resource you want.
- **Query string**: after `?`, `key=value` pairs joined by `&`, usually
  for options such as filters.

A URL may only contain a limited set of characters. Everything else is
**percent-encoded**: each byte of its UTF-8 form becomes `%` plus two hex
digits, so `Malmö` becomes `Malm%C3%B6` and a space becomes `%20` (or
`+` in a query string). `build_url` does this with `urllib.parse.quote`
and `urlencode`. Never glue URLs together with f-strings around raw user
input, for the same reason as SQL in Week 22: a `/`, `?` or `&` inside a
value would change the meaning of the URL.

### What travels over the network

HTTP is a text protocol, so you can read it. Run the practice API and
then `python -m api_client.cli raw /cities/Kiruna`. The request your
program sends looks like this:

```
GET /cities/Kiruna HTTP/1.1
Host: 127.0.0.1:8000
Accept: application/json
User-Agent: basics-course-weather-client/1.0
```

and the response looks like this:

```
HTTP/1.0 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 68

{
  "name": "Kiruna",
  "country": "Sweden",
  "population": 22423
}
```

Both have the same shape: a first line, then **headers** (`Name: value`
metadata), then a blank line, then an optional **body**.

- The request's first line holds the **method** and the path. The method
  says what you want to do with the resource.
- The response's first line holds the **status code**, which says how it
  went. Always check it before trusting the body.
- `Content-Type` says what format the body is in, and `charset=utf-8`
  says how its text is encoded. `Accept` is the client asking for a
  format.

### Methods

| Method | Means | Safe? | Idempotent? |
|---|---|---|---|
| `GET` | read a resource | yes | yes |
| `POST` | create something new (or trigger an action) | no | no |
| `PUT` | replace a resource with the one sent | no | yes |
| `PATCH` | change part of a resource | no | not necessarily |
| `DELETE` | remove a resource | no | yes |

**Safe** means it doesn't change anything on the server. **Idempotent**
means doing it twice has the same effect as doing it once: deleting the
same thing twice leaves it deleted, but posting the same order twice
creates two orders. That difference decides whether it's safe to retry a
request after a timeout, when you can't know whether the first attempt
arrived. The practice API is read-only, so it answers every method except
`GET` with `405 Method Not Allowed` and an `Allow: GET` header.

### Status codes

The first digit is the category:

| Code | Name | Means |
|---|---|---|
| 200 | OK | here's what you asked for |
| 201 | Created | the new resource was made (Week 26) |
| 204 | No Content | done, and there's nothing to send back (Week 26) |
| 400 | Bad Request | your request is malformed (like `from=yesterday`) |
| 401 / 403 | Unauthorized / Forbidden | who are you? / you may not |
| 404 | Not Found | no such resource (or no such endpoint) |
| 405 | Method Not Allowed | this resource doesn't support that method |
| 409 | Conflict | it clashes with the current state (Week 26) |
| 429 | Too Many Requests | slow down: you hit a rate limit |
| 500 | Internal Server Error | the server has a bug |
| 503 | Service Unavailable | the server is down or overloaded; try later |

**4xx means the client's request is the problem**: sending the same
request again gives the same error, so fix the request. **5xx means the
server has the problem**: the same request may work later. `urllib`
raises `HTTPError` for both, and a good API still sends a body explaining
what went wrong; `_error_message` reads that explanation out of the JSON.

### Three different ways a call can fail

```python
try:
    city = client.city("Atlantis")
except ApiError as error:        # the server answered, with a 4xx or 5xx
    ...
except ConnectionError as error: # no answer: wrong address, server down, no network
    ...
```

These need different handling. A 404 is an answer ("there's no such
city") and your program should say so. A connection failure means you
know nothing, and a retry later might work. A third case is the
**timeout**: the server accepted the connection but never answered.
`get_json` passes `timeout=5.0` to `urlopen` because the default is to
wait forever, and a program that hangs forever on a slow network is worse
than one that reports a clear error. (A timeout while reading arrives as
Python's built-in `TimeoutError`.)

### JSON

JSON (JavaScript Object Notation) is how nearly every web API sends
structured data. It's text, and it has six kinds of value, each of which
maps onto a Python type:

| JSON | Python | Example |
|---|---|---|
| object `{...}` | `dict` | `{"name": "Kiruna"}` |
| array `[...]` | `list` | `[1, 2, 3]` |
| string | `str` | `"snow"` (always double quotes) |
| number | `int` or `float` | `22423`, `-3.8` |
| `true` / `false` | `True` / `False` | |
| `null` | `None` | a missing wind reading |

`json.loads(text)` turns JSON text into Python values and `json.dumps`
goes the other way. JSON has no date type, so APIs send dates as text,
almost always in the same ISO-8601 format as Week 19. Note the chain for
a missing wind reading: SQL `NULL` in the server's database, `null` in the
JSON, `None` in your Python code.

### Resource-style URLs (REST)

The practice API's URLs name **things**, not actions: `/cities` is the
collection of cities, `/cities/Kiruna` is one item in it, and
`/cities/Kiruna/observations` is a collection that belongs to that item.
What you want to do with the thing is the method's job (`GET` to read,
`DELETE` to remove). Filters and options that don't identify a different
thing go in the query string (`?from=...&to=...`). This style is called
REST. It's a convention rather than a standard, but it's so common that
you can often guess an API's URLs before reading its documentation.

### Real APIs

A few things you'll meet as soon as you use someone else's API:

- **Documentation is the contract.** Read which endpoints exist, which
  parameters they take, what the JSON looks like, and what the errors
  look like.
- **API keys.** Most APIs want a secret key with each request, usually
  in a header. Keep keys out of your code and out of git: read them from
  an environment variable (`os.environ["WEATHER_API_KEY"]`).
- **Rate limits.** Providers cap how many requests you may make per
  minute or day, and answer `429` beyond that. Don't call an API in a
  tight loop; fetch once and reuse the answer.
- **Identify yourself.** Sending a `User-Agent` that names your program
  is polite and some APIs require it.

`open_meteo.py` calls a real API, [Open-Meteo](https://open-meteo.com),
which is free for non-commercial use and needs no key. Its daily forecast
comes back **column-oriented**, one list per variable:

```json
"daily": {
  "time":               ["2026-10-01", "2026-10-02", "2026-10-03"],
  "temperature_2m_max": [4.1, 2.8, 5.0],
  "temperature_2m_min": [-1.2, -3.4, 0.3],
  "precipitation_sum":  [0.0, 1.6, 0.4]
}
```

That's compact, but the program usually wants one record per day, so
`parse_daily` uses `zip(*columns)`: `zip` walks all the lists in step and
hands back the values at the same position together. (This is the
abridged shape of the response; Open-Meteo's documentation lists every
field.)

## Design & Architecture

```
Week-25-how-apis-work/
├── conftest.py                      - adds src/ to sys.path for pytest
├── src/
│   └── api_client/
│       ├── __init__.py
│       ├── client.py                - build_url, get_json, ApiError, WeatherClient
│       ├── open_meteo.py            - URL and response parsing for the real Open-Meteo API
│       ├── cli.py                   - raw / cities / observations / forecast commands
│       ├── practice_api.py          - the local server to practise on (the subject of Week 26)
│       └── data/
│           └── weather.sql          - the practice API's data (same as Weeks 19-22)
└── tests/
    ├── conftest.py                  - starts the practice API on a free port for the tests
    ├── test_practice_api.py         - the API at the HTTP level: statuses, headers, bodies
    ├── test_client.py               - URL building, the client class, and each kind of failure
    └── test_open_meteo.py           - Open-Meteo, tested offline with a sample response
```

`client.py` has two layers. `build_url` and `get_json` know about HTTP
and JSON but nothing about weather; they'd work with any JSON API.
`WeatherClient` knows the practice API's endpoints and nothing about HTTP
details. A program using it calls `client.observations("Kiruna",
start="2026-09-23")` and gets a list of dicts back, or an exception that
says what went wrong. That's the same pure-logic/thin-I/O split as every
earlier week, applied to a network instead of a file.

The tests start a real practice API server on a free port (port 0 means
"let the operating system pick") in a background thread, and talk to it
over real HTTP. The Open-Meteo tests never touch the network: they check
the URL the code builds and feed `parse_daily` a sample response, so the
suite passes offline and never depends on someone else's server.

## How to Build & Run

You need two terminals, both in the week's folder with `src` on the path:

```bash
cd Month-6-APIs/Week-25-how-apis-work
export PYTHONPATH=src            # PowerShell: $env:PYTHONPATH="src"
```

**Terminal 1**, start the server and leave it running (it prints one line
per request it receives):

```bash
python3 -m api_client.practice_api
```

**Terminal 2**, call it:

```bash
python3 -m api_client.cli raw /cities/Kiruna                 # the whole HTTP response
python3 -m api_client.cli raw /cities/Atlantis               # what a 404 looks like
python3 -m api_client.cli cities
python3 -m api_client.cli observations Kiruna --from 2026-09-23 --to 2026-09-25
python3 -m api_client.cli observations Kiruna --from yesterday   # a 400
python3 -m api_client.cli forecast 67.86 20.23               # real forecast for Kiruna (needs internet)
```

GET requests are just URLs, so you can also open
<http://127.0.0.1:8000/cities/Kiruna/observations> in a browser, or use
`curl -i http://127.0.0.1:8000/cities/Oslo` (`-i` shows the headers).
Stop the server with Ctrl+C, then run a client command again to see what
a `ConnectionError` looks like.

## Testing

```bash
cd Month-6-APIs/Week-25-how-apis-work
python3 -m pytest -q
```

`test_practice_api.py` checks the API as raw HTTP: every endpoint's
status and JSON, the `Content-Type` header, a percent-encoded city name,
`null` for a missing reading, five error cases (unknown city, unknown
endpoint, two kinds of bad date), and `405` with an `Allow` header for
writes. `test_client.py` covers `build_url`'s encoding (non-ASCII, spaces,
a `/` inside a value, query values, skipped `None`s), every
`WeatherClient` method, JSON types arriving as the right Python types,
and the difference between `ApiError` (404, 400) and `ConnectionError`
(nothing listening). `test_open_meteo.py` checks the forecast URL and
`parse_daily`, offline.

## Try It Yourself

1. Add `WeatherClient.warmest_day(city)`, which fetches a city's
   observations and returns the one with the highest `temp_max_c`. Should
   it make one request or several? Write the test first, using the
   `base_url` fixture.
2. Give `get_json` a `retries` parameter: on a `ConnectionError` or a
   5xx `ApiError`, wait 1 second and try again, up to `retries` times, but
   never retry a 4xx. Explain in a comment why the two are treated
   differently. (Testing the 5xx case needs a server that fails; how
   could you make one?)
3. Extend `open_meteo.py` to also request `wind_speed_10m_max`, and add
   it to `DailyForecast`. Check Open-Meteo's documentation for its unit,
   and convert it to m/s if needed so it matches the rest of this course.
4. Write a `compare` CLI command that prints, for one city, the
   practice API's observation for a date next to Open-Meteo's *forecast*
   for the same coordinates. What do you need to know about each city
   that the practice API doesn't provide?
5. Use `curl` to send a `DELETE` to the practice API and read the full
   response with `-i`. Which header tells a client what it may do
   instead, and which status code would you expect if the API did
   support deleting but the city didn't exist?
