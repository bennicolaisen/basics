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

    def test_negative(self):
        assert celsius_to_fahrenheit(-40) == pytest.approx(-40.0)

    def test_roundtrip(self):
        c = 23.5
        assert fahrenheit_to_celsius(celsius_to_fahrenheit(c)) == pytest.approx(c)


class TestFahrenheitToCelsius:
    def test_freezing_point(self):
        assert fahrenheit_to_celsius(32) == pytest.approx(0.0)

    def test_negative(self):
        assert fahrenheit_to_celsius(-40) == pytest.approx(-40.0)

    def test_body_temp(self):
        assert fahrenheit_to_celsius(98.6) == pytest.approx(37.0, abs=1e-2)


class TestKmToMiles:
    def test_zero(self):
        assert km_to_miles(0) == pytest.approx(0.0)

    def test_known_value(self):
        # 1 mile is exactly 1.609344 km, so 1.609344 km is exactly 1 mile.
        assert km_to_miles(1.609344) == pytest.approx(1.0)

    def test_roundtrip(self):
        km = 42.195  # marathon distance
        assert miles_to_km(km_to_miles(km)) == pytest.approx(km)


class TestMilesToKm:
    def test_zero(self):
        assert miles_to_km(0) == pytest.approx(0.0)

    def test_known_value(self):
        assert miles_to_km(1) == pytest.approx(1.609344)

    def test_negative(self):
        # Negative distance is unusual but mathematically well-defined
        # (e.g. displacement), so it's not rejected here.
        assert miles_to_km(-1) == pytest.approx(-1.609344)


class TestSecondsToHms:
    def test_zero(self):
        assert seconds_to_hms(0) == (0, 0, 0)

    def test_only_seconds(self):
        assert seconds_to_hms(45) == (0, 0, 45)

    def test_exactly_one_minute(self):
        assert seconds_to_hms(60) == (0, 1, 0)

    def test_exactly_one_hour(self):
        assert seconds_to_hms(3600) == (1, 0, 0)

    def test_mixed(self):
        # 1h 1m 1s = 3661 seconds
        assert seconds_to_hms(3661) == (1, 1, 1)

    def test_just_under_an_hour(self):
        assert seconds_to_hms(3599) == (0, 59, 59)

    def test_large_value_multiple_days_worth(self):
        # 90061 seconds = 25h 1m 1s (hours are not capped at 24)
        assert seconds_to_hms(90061) == (25, 1, 1)

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            seconds_to_hms(-1)
