"""Starta veckans gissningsspel. Skriv i terminalen (i den här mappen):

    python starta.py

(På Mac och Linux heter kommandot ofta python3.)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from validators_and_games.game import main  # noqa: E402  (måste komma efter raden ovan)

main()
