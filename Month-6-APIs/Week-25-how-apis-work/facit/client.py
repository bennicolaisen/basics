"""Facit vecka 25, uppgift 1 och 2. Se FACIT.md."""

import time

from api_client import client as original
from api_client.client import ApiError, WeatherClient, build_url  # noqa: F401


def get_json(url: str, timeout: float = 5.0, retries: int = 0, retry_delay: float = 1.0, sleep=time.sleep) -> object:
    """Som api_client.client.get_json, men försöker igen vid tillfälliga fel.

    Ett ConnectionError eller ett 5xx-svar försöks igen upp till `retries`
    gånger, med `retry_delay` sekunder emellan. Ett 4xx-svar försöks aldrig
    igen.

    Varför olika? Ett 4xx betyder att det är FRÅGAN som är fel (en stad som
    inte finns, ett datum i fel format). Samma fråga en gång till får samma
    svar, så det enda ett nytt försök gör är att belasta servern och låta
    användaren vänta. Ett 5xx eller ett uteblivet svar betyder att något gick
    fel hos servern eller på vägen dit (överbelastning, omstart, nätverket),
    och det kan mycket väl fungera om en stund.

    `sleep` är en parameter så att testerna kan byta ut väntan mot ingenting.
    """
    if retries < 0:
        raise ValueError("retries must be 0 or more")
    for attempt in range(retries + 1):
        try:
            return original.get_json(url, timeout=timeout)
        except ApiError as error:
            if error.status < 500 or attempt == retries:
                raise
        except ConnectionError:
            if attempt == retries:
                raise
        sleep(retry_delay)
    raise AssertionError("unreachable")  # loopen returnerar eller kastar alltid


class FacitWeatherClient(WeatherClient):
    """WeatherClient med uppgift 1: warmest_day."""

    def warmest_day(self, city: str) -> dict:
        """Observationen med högst temp_max_c. Vid lika vinner den tidigaste dagen.

        En enda förfrågan räcker: API:et skickar alla observationer på en
        gång, och att hitta den varmaste är enkelt i Python.
        """
        observations = self.observations(city)
        if not observations:
            raise ValueError(f"{city} has no observations")
        return max(observations, key=lambda observation: observation["temp_max_c"])
