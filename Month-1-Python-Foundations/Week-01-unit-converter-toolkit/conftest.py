"""Gör veckans kod och övningar åtkomliga för pytest.

- `src/` läggs till på Pythons sökväg, så att testerna kan importera
  veckans projekt.
- Kontrollerna i `kontroll/` testar dina lösningar i `ovningar/`. Med
  flaggan `--facit` testar de i stället lösningarna i `facit/`:

      python -m pytest kontroll            # kontrollera dina lösningar
      python -m pytest kontroll -k 05      # bara övning 5
      python -m pytest kontroll --facit    # visa att facit klarar allt
"""

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

WEEK_DIR = Path(__file__).parent
SRC = WEEK_DIR / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def pytest_addoption(parser):
    parser.addoption("--facit", action="store_true", help="kontrollera facit/ i stället för ovningar/")


def _exercise_path(config, name: str) -> Path:
    folder = "facit" if config.getoption("--facit") else "ovningar"
    return WEEK_DIR / folder / f"{name}.py"


@pytest.fixture
def kallkod(request):
    """Texten i en övningsfil, för kontroller av regler som "bara ett anrop till print"."""

    def read(name: str) -> str:
        return _exercise_path(request.config, name).read_text(encoding="utf-8")

    return read


@pytest.fixture
def ovning(request):
    """Laddar en övningsfil som innehåller funktioner, till exempel ovning("10_avrunda")."""

    def load(name: str):
        spec = importlib.util.spec_from_file_location(name, _exercise_path(request.config, name))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    return load


@pytest.fixture
def kor(request, monkeypatch, capsys):
    """Kör en övningsfil som ett program.

    - `inmatning`: det som "skrivs in" vid varje input(), i tur och ordning.
    - `ersatt`: rader i filen som byts ut innan programmet körs, till
      exempel {"a = 7": "a = 'hej'"}, för att prova med andra startvärden.

    Returnerar ett objekt med `.utskrift` (allt programmet skrev ut, med
    inmatningen ekad som i en terminal) och `.variabler` (programmets
    variabler när det kört klart).
    """

    def run(name: str, inmatning=(), ersatt=None):
        path = _exercise_path(request.config, name)
        source = path.read_text(encoding="utf-8")
        for old, new in (ersatt or {}).items():
            if old not in source:
                raise AssertionError(f"Raden {old!r} ska stå kvar oförändrad i filen.")
            source = source.replace(old, new, 1)

        answers = list(inmatning)

        def fake_input(prompt=""):
            print(prompt, end="")
            if not answers:
                raise AssertionError("Programmet frågade efter mer inmatning än uppgiften säger.")
            value = answers.pop(0)
            print(value)
            return value

        monkeypatch.setattr("builtins.input", fake_input)
        variables = {"__name__": "__main__", "__file__": str(path)}
        exec(compile(source, str(path), "exec"), variables)
        return SimpleNamespace(utskrift=capsys.readouterr().out, variabler=variables)

    return run
