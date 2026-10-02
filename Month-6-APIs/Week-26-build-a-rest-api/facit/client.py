"""Facit vecka 26, uppgift 5: vecka 25:s WeatherClient med add_observation.

Klienten finns i vecka 25:s mapp. Här läggs den mappen till i sys.path så
att den kan importeras; i ett riktigt projekt skulle klienten vara ett eget
paket som installeras med pip.
"""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

WEEK_25_SRC = Path(__file__).resolve().parents[2] / "Week-25-how-apis-work" / "src"
if str(WEEK_25_SRC) not in sys.path:
    sys.path.insert(0, str(WEEK_25_SRC))

from api_client.client import USER_AGENT, ApiError, WeatherClient, _error_message, build_url  # noqa: E402


def send_json(method: str, url: str, payload: object, headers: dict[str, str] | None = None, timeout: float = 5.0) -> object:
    """Skicka `payload` som JSON med `method` och returnera svarets JSON (None om svaret saknar kropp)."""
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method=method,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
            **(headers or {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as error:
        raise ApiError(error.code, _error_message(error)) from None
    except urllib.error.URLError as error:
        raise ConnectionError(f"could not reach {url}: {error.reason}") from None
    return json.loads(raw.decode("utf-8")) if raw else None


class FacitWeatherClient(WeatherClient):
    def __init__(self, base_url: str = "http://127.0.0.1:8000", api_key: str | None = None):
        super().__init__(base_url)
        self.api_key = api_key

    def add_observation(self, city: str, observation: dict) -> dict:
        """POST:a en observation och returnera den som servern sparade.

        400 (ogiltiga värden), 404 (ingen sådan stad), 409 (dagen finns redan)
        och 401 (fel nyckel) blir ApiError med statuskoden i `.status`.
        """
        headers = {"X-API-Key": self.api_key} if self.api_key else {}
        url = build_url(self.base_url, ["cities", city, "observations"])
        return send_json("POST", url, observation, headers)
