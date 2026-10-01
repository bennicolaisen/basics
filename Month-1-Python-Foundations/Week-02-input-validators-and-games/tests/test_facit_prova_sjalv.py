"""Tester för facit till "Prova själv" (facit/prova_sjalv.py)."""

import pytest

from facit.prova_sjalv import (
    count_valid_usernames,
    is_valid_email,
    main_with_difficulty,
    main_with_tally,
    play_game_strict,
)


def fake_answers(monkeypatch, answers):
    remaining = list(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": remaining.pop(0))


@pytest.mark.parametrize(
    "text, expected",
    [
        ("alva@example.se", True),
        ("a.b@mail.example.com", True),
        ("", False),
        ("alva.example.se", False),     # inget @
        ("alva@@example.se", False),    # två @
        ("@example.se", False),         # inget före @
        ("alva@examplese", False),      # ingen punkt efter @
        ("alva@.se", False),            # punkt direkt efter @
        ("alva@example.", False),       # punkt sist
        ("al va@example.se", False),    # mellanslag
    ],
)
def test_1_is_valid_email(text, expected):
    assert is_valid_email(text) is expected


def test_2_invalid_guess_costs_an_attempt(monkeypatch, capsys):
    fake_answers(monkeypatch, ["hej", "5"])
    assert play_game_strict(5, 1, 10, 1) is False  # första försöket gick åt till "hej"
    assert "Det kostade ett försök. 0 försök kvar." in capsys.readouterr().out


def test_2_valid_guess_still_wins(monkeypatch):
    fake_answers(monkeypatch, ["oj", "5"])
    assert play_game_strict(5, 1, 10, 2) is True


def test_3_difficulty_sets_range_and_attempts(monkeypatch, capsys):
    monkeypatch.setattr("random.randint", lambda low, high: high)  # svaret blir alltid det högsta talet
    fake_answers(monkeypatch, ["superlätt", "Lätt", "10"])
    assert main_with_difficulty() is True
    out = capsys.readouterr().out
    assert "Skriv lätt, medel eller svår." in out
    assert "Jag tänker på ett tal mellan 1 och 10." in out
    assert "Du har 5 försök." in out


def test_4_count_valid_usernames():
    assert count_valid_usernames(["alva_1", "1bo", "x", "Charlie"]) == 2
    assert count_valid_usernames([]) == 0


def test_5_tally_counts_wins_and_losses(monkeypatch, capsys):
    monkeypatch.setattr("random.randint", lambda low, high: 50)
    fake_answers(monkeypatch, ["50", "j"] + ["1"] * 7 + ["n"])
    assert main_with_tally() == (1, 1)
    assert "Vinster: 1, förluster: 1" in capsys.readouterr().out
