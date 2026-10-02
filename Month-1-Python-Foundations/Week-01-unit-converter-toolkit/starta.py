"""Starta veckans program. Skriv i terminalen (i den här mappen):

    python starta.py

(På Mac och Linux heter kommandot ofta python3.)
"""

import sys
from pathlib import Path

# Säg åt Python att leta efter veckans kod i mappen src/.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from converter_toolkit.cli import main  # noqa: E402  (måste komma efter raden ovan)

main()
