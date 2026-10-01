"""A real, public API: daily forecasts from Open-Meteo (https://open-meteo.com).

Open-Meteo is free for non-commercial use and needs no API key, which
makes it a good first real API. Its daily forecast comes back
"column-oriented": one list per variable, all the same length, where
position i in every list belongs to the same day. `parse_daily` zips
those columns back into one record per day.
"""

from dataclasses import dataclass
from urllib.parse import urlencode

from api_client.client import get_json

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
DAILY_VARIABLES = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]


@dataclass(frozen=True)
class DailyForecast:
    day: str
    temp_max_c: float
    temp_min_c: float
    precipitation_mm: float


def forecast_url(latitude: float, longitude: float, days: int = 3) -> str:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join(DAILY_VARIABLES),
        "timezone": "auto",  # report days in the location's own time zone
        "forecast_days": days,
    }
    return f"{FORECAST_URL}?{urlencode(params)}"


def parse_daily(payload: dict) -> list[DailyForecast]:
    daily = payload["daily"]
    columns = [daily["time"]] + [daily[name] for name in DAILY_VARIABLES]
    return [DailyForecast(*values) for values in zip(*columns)]


def fetch_forecast(latitude: float, longitude: float, days: int = 3) -> list[DailyForecast]:
    """Call the live API (needs an internet connection)."""
    return parse_daily(get_json(forecast_url(latitude, longitude, days)))
