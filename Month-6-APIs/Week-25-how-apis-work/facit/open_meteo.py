"""Facit vecka 25, uppgift 3: Open-Meteo med daglig maxvind i m/s. Se FACIT.md."""

from dataclasses import dataclass
from datetime import date
from urllib.parse import urlencode

from api_client.client import get_json
from api_client.open_meteo import FORECAST_URL

DAILY_VARIABLES = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"]

# Open-Meteo anger vind i km/h om man inte ber om något annat.
# 1 km/h = 1000 m / 3600 s, alltså delar man med 3,6 för att få m/s.
WIND_TO_MS = {"m/s": 1.0, "km/h": 1 / 3.6}


@dataclass(frozen=True)
class DailyForecast:
    day: str
    temp_max_c: float
    temp_min_c: float
    precipitation_mm: float
    wind_max_ms: float


def forecast_url(latitude: float, longitude: float, days: int = 3, past_days: int = 0) -> str:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join(DAILY_VARIABLES),
        "timezone": "auto",
        "forecast_days": days,
        "wind_speed_unit": "ms",  # be om m/s direkt
    }
    if past_days:
        params["past_days"] = past_days
    return f"{FORECAST_URL}?{urlencode(params)}"


def parse_daily(payload: dict) -> list[DailyForecast]:
    """Gör om kolumnerna till en post per dag, med vinden omräknad till m/s.

    Vi ber om m/s, men läser ändå enheten ur svaret (daily_units) i stället
    för att lita på det. Får vi km/h räknar vi om; får vi något helt annat
    är det bättre att säga ifrån än att visa fel siffror.
    """
    daily = payload["daily"]
    unit = payload.get("daily_units", {}).get("wind_speed_10m_max", "km/h")
    if unit not in WIND_TO_MS:
        raise ValueError(f"unexpected wind speed unit: {unit!r}")
    factor = WIND_TO_MS[unit]
    rows = zip(daily["time"], *(daily[name] for name in DAILY_VARIABLES))
    return [
        DailyForecast(day, temp_max, temp_min, precipitation, None if wind is None else round(wind * factor, 1))
        for day, temp_max, temp_min, precipitation, wind in rows
    ]


def fetch_forecast(latitude: float, longitude: float, days: int = 3) -> list[DailyForecast]:
    return parse_daily(get_json(forecast_url(latitude, longitude, days)))


def fetch_day(latitude: float, longitude: float, day: str, today: date | None = None) -> DailyForecast:
    """Open-Meteos värden för en enda dag, högst 92 dagar bakåt eller 15 dagar framåt."""
    today = today or date.today()
    offset = (date.fromisoformat(day) - today).days
    if not -92 <= offset <= 15:
        raise ValueError(f"Open-Meteo's forecast covers 92 days back to 15 days ahead; {day} is outside that")
    url = forecast_url(latitude, longitude, days=max(1, offset + 1), past_days=max(0, -offset))
    for forecast in parse_daily(get_json(url)):
        if forecast.day == day:
            return forecast
    raise ValueError(f"Open-Meteo returned no values for {day}")
