"""Tester för converters.py.

Varje test anropar en funktion med ett tal vi vet svaret på och kollar
att funktionen returnerar rätt. pytest.approx betyder "ungefär lika
med": decimaltal i datorer kan bli en aning fel i sista decimalen, så
vi jämför inte dem med ==. Se steg 9 i README.
"""

import pytest

from converter_toolkit.converters import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    km_to_miles,
    miles_to_km,
    seconds_to_hms,
)


class TestCelsiusToFahrenheit:
    def test_freezing_point(self):
        assert celsius_to_fahrenheit(0) == pytest.approx(32.0)

    def test_boiling_point(self):
        assert celsius_to_fahrenheit(100) == pytest.approx(212.0)

    def test_minus_forty_is_the_same_in_both(self):
        assert celsius_to_fahrenheit(-40) == pytest.approx(-40.0)

    def test_round_trip(self):
        assert fahrenheit_to_celsius(celsius_to_fahrenheit(23.5)) == pytest.approx(23.5)


class TestFahrenheitToCelsius:
    def test_freezing_point(self):
        assert fahrenheit_to_celsius(32) == pytest.approx(0.0)

    def test_body_temperature(self):
        assert fahrenheit_to_celsius(98.6) == pytest.approx(37.0)


class TestDistances:
    def test_zero_km(self):
        assert km_to_miles(0) == pytest.approx(0.0)

    def test_one_mile_in_km(self):
        assert miles_to_km(1) == pytest.approx(1.609344)

    def test_one_mile_back_again(self):
        assert km_to_miles(1.609344) == pytest.approx(1.0)

    def test_marathon_round_trip(self):
        assert miles_to_km(km_to_miles(42.195)) == pytest.approx(42.195)


class TestSecondsToHms:
    def test_zero(self):
        assert seconds_to_hms(0) == "0:00:00"

    def test_only_seconds(self):
        assert seconds_to_hms(45) == "0:00:45"

    def test_exactly_one_minute(self):
        assert seconds_to_hms(60) == "0:01:00"

    def test_exactly_one_hour(self):
        assert seconds_to_hms(3600) == "1:00:00"

    def test_mixed(self):
        assert seconds_to_hms(3665) == "1:01:05"

    def test_just_under_an_hour(self):
        assert seconds_to_hms(3599) == "0:59:59"

    def test_hours_keep_counting_past_24(self):
        assert seconds_to_hms(90061) == "25:01:01"
