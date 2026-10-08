"""Tester för facit till "Prova själv" (facit/prova_sjalv.py).

Uppgift 5 är själv ett test, så dess facit är de två sista testerna här.
"""

from pathlib import Path

import pytest

from converter_toolkit.converters import seconds_to_hms
from facit.prova_sjalv import (
    celsius_to_kelvin,
    hms_to_seconds,
    kelvin_to_celsius,
    kmh_to_mph,
    main,
    mph_to_kmh,
    pace,
)


def test_1_kelvin():
    assert celsius_to_kelvin(0) == pytest.approx(273.15)
    assert kelvin_to_celsius(0) == pytest.approx(-273.15)
    assert celsius_to_kelvin(-273.15) == pytest.approx(0)
    assert kelvin_to_celsius(celsius_to_kelvin(21.5)) == pytest.approx(21.5)


@pytest.mark.parametrize("text, seconds", [("0:00:00", 0), ("1:01:05", 3665), ("25:00:00", 90000), ("100:59:59", 363599)])
def test_2_hms_to_seconds(text, seconds):
    assert hms_to_seconds(text) == seconds


@pytest.mark.parametrize("seconds", [0, 59, 60, 3599, 3600, 86399, 90061, 1_000_000])
def test_2_is_the_inverse_of_seconds_to_hms(seconds):
    assert hms_to_seconds(seconds_to_hms(seconds)) == seconds


@pytest.mark.parametrize(
    "km, minutes, expected",
    [(10, 55, "5:30 min/km"), (5, 29.99, "6:00 min/km"), (42.195, 180, "4:16 min/km"), (1, 3.5, "3:30 min/km")],
)
def test_3_pace(km, minutes, expected):
    assert pace(km, minutes) == expected


def test_4_speed_conversions():
    assert mph_to_kmh(60) == pytest.approx(96.56064)
    assert kmh_to_mph(mph_to_kmh(70)) == pytest.approx(70)


def test_4_the_factor_is_written_only_once():
    facit_source = (Path(__file__).parent.parent / "facit" / "prova_sjalv.py").read_text(encoding="utf-8")
    assert "1.609344" not in facit_source


def test_4_cli_asks_for_speed_last(monkeypatch, capsys):
    answers = iter(["20", "10", "60", "100"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    main()
    assert capsys.readouterr().out.splitlines()[-1] == "100.0 km/h är 62.1 mph"


def test_5_floats_are_not_exact():
    # 0.1 och 0.2 kan inte lagras exakt binärt, så summan blir en aning fel.
    assert 0.1 + 0.2 != 0.3


def test_5_approx_compares_with_a_tolerance():
    assert 0.1 + 0.2 == pytest.approx(0.3)
