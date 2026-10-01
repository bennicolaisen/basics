"""Tester för facit till "Prova själv" (facit/prova_sjalv.py).

Uppgift 5 ("visa att 0.1 + 0.2 inte blir exakt 0.3") är själv ett test,
så dess facit är de två sista testerna i den här filen.
"""

import pytest

from converter_toolkit.converters import seconds_to_hms
from facit.prova_sjalv import (
    celsius_to_kelvin,
    hms_to_seconds,
    kelvin_to_celsius,
    kmh_to_mph,
    main,
    mph_to_kmh,
)


def test_1_zero_celsius_is_273_kelvin():
    assert celsius_to_kelvin(0) == pytest.approx(273.15)


def test_1_absolute_zero():
    assert kelvin_to_celsius(0) == pytest.approx(-273.15)


def test_1_round_trip():
    assert kelvin_to_celsius(celsius_to_kelvin(21.5)) == pytest.approx(21.5)


def test_2_hms_to_seconds():
    assert hms_to_seconds(1, 1, 5) == 3665


def test_2_is_the_inverse_of_seconds_to_hms():
    assert seconds_to_hms(hms_to_seconds(25, 1, 1)) == "25:01:01"


def test_3_speed_conversions():
    assert mph_to_kmh(60) == pytest.approx(96.56064)
    assert kmh_to_mph(mph_to_kmh(70)) == pytest.approx(70)


def test_4_cli_asks_for_speed_last(monkeypatch, capsys):
    answers = iter(["20", "10", "60", "100"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    main()
    assert capsys.readouterr().out.splitlines()[-1] == "100.0 km/h är 62.1 mph"


def test_5_floats_are_not_exact():
    # 0.1 och 0.2 kan inte lagras exakt i datorns binära talsystem (precis
    # som 1/3 inte kan skrivas exakt med decimaler), så summan blir en aning fel.
    assert 0.1 + 0.2 != 0.3
    assert 0.1 + 0.2 == 0.30000000000000004


def test_5_approx_compares_with_a_tolerance():
    # pytest.approx godtar en mycket liten skillnad, så testet handlar om
    # att räkningen är rätt, inte om datorns sista decimal.
    assert 0.1 + 0.2 == pytest.approx(0.3)
