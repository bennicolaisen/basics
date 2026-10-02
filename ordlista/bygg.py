"""Bygg ORDLISTA.md och ordlista/index.html från ordlista/termer.json.

    python ordlista/bygg.py

termer.json är den enda källan: lägg till eller ändra ord där och kör
skriptet. Testet i test_ordlista.py misslyckas om de byggda filerna inte
är uppdaterade.
"""

import json
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
TERMS_FILE = HERE / "termer.json"
TEMPLATE_FILE = HERE / "mall.html"
MARKDOWN_FILE = ROOT / "ORDLISTA.md"
HTML_FILE = HERE / "index.html"

PARTS = [
    (1, 4, "Python-grunder"),
    (5, 8, "Rekursion, datastrukturer och algoritmer"),
    (9, 12, "Objektorientering och Java"),
    (13, 18, "Undantag, testning, felsökning och Git"),
    (19, 24, "Databaser och SQL"),
    (25, 26, "API:er"),
]

INTRO = """# Ordlista

Alla ord och begrepp i kursen, med det engelska ordet (som står i koden
och i de flesta böcker och sökresultat), en svensk översättning och en
förklaring. Orden är ordnade efter den del av kursen där de först dyker
upp.

## Öva och bli förhörd

**I webbläsaren:** öppna [`ordlista/index.html`](ordlista/index.html).
Där kan du läsa orden, öva med glosskort och göra förhör. Sidan kommer
ihåg vilka ord du kan.

**I terminalen** (i kursens huvudmapp):

```
python ordlista/ova.py                      # 10 frågor från hela kursen
python ordlista/ova.py --vecka 1-4          # bara orden från vecka 1–4
python ordlista/ova.py --antal 20 --typ skriv
python ordlista/ova.py --lista --vecka 2    # visa veckans glosor
```

Förhöret blandar två sorters frågor: antingen får du förklaringen och
skriver det engelska ordet, eller så får du ordet och väljer rätt
förklaring av fyra. Efteråt ser du vilka ord du missade och kan öva på
dem direkt.
"""


def load_terms() -> list[dict]:
    with open(TERMS_FILE, encoding="utf-8") as file:
        return json.load(file)


def markdown_cell(text: str) -> str:
    return text.replace("|", "\\|")


def build_markdown(terms: list[dict]) -> str:
    sections = [INTRO]
    for first, last, title in PARTS:
        part = sorted(
            [t for t in terms if first <= t["vecka"] <= last],
            key=lambda t: (t["vecka"], t["term"].lower()),
        )
        lines = [
            f"## {title} (vecka {first}–{last})",
            "",
            "| Engelska | Svenska | Förklaring | Vecka |",
            "|---|---|---|---|",
        ]
        for term in part:
            explanation = term["forklaring"]
            if "exempel" in term:
                explanation += f" Exempel: `{term['exempel']}`"
            lines.append(
                f"| **{markdown_cell(term['term'])}** | {markdown_cell(term['sv'])} "
                f"| {markdown_cell(explanation)} | {term['vecka']} |"
            )
        sections.append("\n".join(lines))
    return "\n\n".join(sections) + "\n"


def build_html(terms: list[dict]) -> str:
    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    parts = [{"first": first, "last": last, "title": title} for first, last, title in PARTS]
    data = json.dumps({"terms": terms, "parts": parts}, ensure_ascii=False)
    # "</" inuti en <script> skulle kunna avsluta skriptet i förtid.
    return template.replace("__ORDLISTA_DATA__", data.replace("</", "<\\/"))


def main() -> None:
    terms = load_terms()
    MARKDOWN_FILE.write_text(build_markdown(terms), encoding="utf-8")
    HTML_FILE.write_text(build_html(terms), encoding="utf-8")
    print(f"Byggde {MARKDOWN_FILE.name} och {HTML_FILE.relative_to(ROOT)} med {len(terms)} ord.")


if __name__ == "__main__":
    main()
