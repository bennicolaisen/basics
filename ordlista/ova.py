"""Öva på kursens ordlista i terminalen och bli förhörd.

    python ordlista/ova.py                      # 10 frågor från hela kursen
    python ordlista/ova.py --vecka 1-4          # bara orden från vecka 1–4
    python ordlista/ova.py --antal 20           # 20 frågor
    python ordlista/ova.py --typ skriv          # skriv det engelska ordet
    python ordlista/ova.py --typ flerval        # välj rätt förklaring
    python ordlista/ova.py --lista --vecka 2    # visa glosorna utan förhör

Två sorters frågor blandas:

- *skriv*: du får den svenska förklaringen och skriver det engelska ordet.
- *flerval*: du får det engelska ordet och väljer rätt förklaring av fyra.

Efter förhöret får du se resultatet och vilka ord du missade, och kan öva
direkt på just dem.
"""

import argparse
import json
import random
import sys
from pathlib import Path

TERMS_FILE = Path(__file__).parent / "termer.json"
CHOICE_LETTERS = "abcd"


def load_terms(path: Path = TERMS_FILE) -> list[dict]:
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def parse_weeks(text: str) -> tuple[int, int]:
    """'3' ger (3, 3) och '1-4' ger (1, 4)."""
    parts = text.replace("–", "-").split("-")
    try:
        numbers = [int(part) for part in parts]
    except ValueError:
        raise ValueError(f"veckor anges som 3 eller 1-4, inte {text!r}") from None
    if len(numbers) == 1:
        return numbers[0], numbers[0]
    if len(numbers) == 2 and numbers[0] <= numbers[1]:
        return numbers[0], numbers[1]
    raise ValueError(f"veckor anges som 3 eller 1-4, inte {text!r}")


def terms_for_weeks(terms: list[dict], first: int, last: int) -> list[dict]:
    return [term for term in terms if first <= term["vecka"] <= last]


def normalize(text: str) -> str:
    """Gemener, inga mellanslag runt omkring och enkla mellanslag inuti."""
    return " ".join(text.lower().split())


def is_correct(answer: str, term: dict) -> bool:
    """Godta det engelska ordet eller något av dess alternativ, utan hänsyn till stora bokstäver."""
    accepted = [term["term"]] + term.get("alternativ", [])
    return normalize(answer) in [normalize(word) for word in accepted]


def make_choices(term: dict, terms: list[dict], rng: random.Random, count: int = 4) -> list[dict]:
    """Rätt term plus count - 1 andra, i slumpad ordning."""
    others = [other for other in terms if other["term"] != term["term"]]
    choices = rng.sample(others, min(count - 1, len(others))) + [term]
    rng.shuffle(choices)
    return choices


def ask_write(term: dict, ask, tell) -> bool:
    tell(f"\n{term['forklaring']}")
    tell(f"(på svenska: {term['sv']})")
    answer = ask("Engelskt ord: ")
    if is_correct(answer, term):
        tell("Rätt!")
        return True
    tell(f"Fel. Rätt svar: {term['term']}")
    return False


def ask_choice(term: dict, terms: list[dict], rng: random.Random, ask, tell) -> bool:
    choices = make_choices(term, terms, rng)
    tell(f"\nVad betyder {term['term']}?")
    for letter, choice in zip(CHOICE_LETTERS, choices):
        tell(f"  {letter}) {choice['forklaring']}")
    correct_letter = CHOICE_LETTERS[choices.index(term)]
    answer = normalize(ask("Svar (a–d): "))
    if answer == correct_letter:
        tell(f"Rätt! {term['term']} = {term['sv']}")
        return True
    tell(f"Fel. Rätt svar: {correct_letter}) {term['term']} = {term['sv']}")
    return False


def run_quiz(questions: list[dict], all_terms: list[dict], kind: str, rng: random.Random, ask, tell) -> list[dict]:
    """Ställ frågorna och returnera de termer som besvarades fel.

    kind är "skriv", "flerval" eller "blandat". ask och tell är input och
    print när programmet körs, men kan bytas ut i tester.
    """
    missed = []
    for number, term in enumerate(questions, start=1):
        tell(f"\n--- Fråga {number} av {len(questions)} ---")
        question_kind = kind if kind != "blandat" else rng.choice(["skriv", "flerval"])
        if question_kind == "skriv":
            correct = ask_write(term, ask, tell)
        else:
            correct = ask_choice(term, all_terms, rng, ask, tell)
        if not correct:
            missed.append(term)
    score = len(questions) - len(missed)
    tell(f"\nResultat: {score} av {len(questions)} rätt.")
    if missed:
        tell("Öva mer på:")
        for term in missed:
            tell(f"  {term['term']} = {term['sv']}: {term['forklaring']}")
    return missed


def print_list(terms: list[dict], tell) -> None:
    for term in sorted(terms, key=lambda t: (t["vecka"], t["term"].lower())):
        tell(f"v{term['vecka']:<3}{term['term']:<28}{term['sv']}")
        tell(f"     {term['forklaring']}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Öva på kursens ordlista.")
    parser.add_argument("--vecka", default="1-26", help="en vecka (3) eller ett intervall (1-4); standard: hela kursen")
    parser.add_argument("--antal", type=int, default=10, help="antal frågor (standard 10)")
    parser.add_argument("--typ", choices=["blandat", "skriv", "flerval"], default="blandat")
    parser.add_argument("--lista", action="store_true", help="visa glosorna i stället för att förhöra")
    args = parser.parse_args(argv)

    try:
        first, last = parse_weeks(args.vecka)
    except ValueError as error:
        sys.exit(f"Fel: {error}")
    all_terms = load_terms()
    terms = terms_for_weeks(all_terms, first, last)
    if not terms:
        sys.exit(f"Det finns inga ord för vecka {args.vecka}.")

    if args.lista:
        print_list(terms, print)
        return

    rng = random.Random()
    questions = rng.sample(terms, min(args.antal, len(terms)))
    print(f"Ordförhör: {len(questions)} frågor från vecka {first}–{last}. Avbryt med Ctrl+C.")
    try:
        missed = run_quiz(questions, all_terms, args.typ, rng, input, print)
        while missed and normalize(input("\nÖva igen på de du missade? (j/n) ")) == "j":
            missed = run_quiz(missed, all_terms, args.typ, rng, input, print)
    except (KeyboardInterrupt, EOFError):
        print("\nHej då!")


if __name__ == "__main__":
    main()
