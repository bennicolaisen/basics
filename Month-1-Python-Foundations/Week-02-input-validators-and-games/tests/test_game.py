"""Tester för gissningsspelet.

Spelet frågar med input(), så testerna byter ut input mot en funktion
som "skriver in" färdiga svar. monkeypatch är pytests verktyg för att
tillfälligt byta ut något under ett test.
"""

from validators_and_games.game import play_game


def fake_answers(monkeypatch, answers):
    remaining = list(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": remaining.pop(0))


def test_correct_first_guess_wins(monkeypatch, capsys):
    fake_answers(monkeypatch, ["42"])
    assert play_game(42, 1, 100, 7) is True
    assert "Rätt! Talet var 42. Du klarade det på 1 försök." in capsys.readouterr().out


def test_hints_lead_to_the_answer(monkeypatch, capsys):
    fake_answers(monkeypatch, ["50", "25", "37"])
    assert play_game(37, 1, 100, 7) is True
    out = capsys.readouterr().out
    assert "För högt. 6 försök kvar." in out
    assert "För lågt. 5 försök kvar." in out


def test_running_out_of_attempts_loses(monkeypatch, capsys):
    fake_answers(monkeypatch, ["1", "2", "3"])
    assert play_game(99, 1, 100, 3) is False
    assert "Slut på försök. Talet var 99." in capsys.readouterr().out


def test_invalid_guess_does_not_cost_an_attempt(monkeypatch, capsys):
    fake_answers(monkeypatch, ["hej", "500", "5"])
    assert play_game(5, 1, 10, 1) is True
    out = capsys.readouterr().out
    assert "Ogiltig gissning: 'hej' är inte ett heltal" in out
    assert "Ogiltig gissning: 500 ligger utanför 1–10" in out
