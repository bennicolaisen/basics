"""Analysera en text. Skriv i terminalen (i den här mappen):

    python starta.py                  # den medföljande exempeltexten
    python starta.py min_text.txt     # en egen textfil

(På Mac och Linux heter kommandot ofta python3.)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from text_analyzer.cli import main  # noqa: E402  (måste komma efter raden ovan)

main()
