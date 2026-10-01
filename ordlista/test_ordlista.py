"""Tester för ordlistan: datan, de byggda filerna och förhöret i ova.py.

    python -m pytest ordlista
"""

import random

import pytest

import bygg
import ova

TERMS = ova.load_terms()


class TestData:
    def test_every_term_has_the_required_fields(self):
        for term in TERMS:
            assert set(term) >= {"term", "sv", "forklaring", "vecka"}, term
            assert term["term"].strip() and term["sv"].strip() and term["forklaring"].strip(), term
            assert isinstance(term["vecka"], int) and 1 <= term["vecka"] <= 26, term

    def test_explanations_are_full_sentences(self):
        for term in TERMS:
            assert term["forklaring"][0].isupper(), term["term"]
            assert term["forklaring"].endswith("."), term["term"]

    def test_no_duplicate_terms(self):
        names = [term["term"].lower() for term in TERMS]
        assert len(names) == len(set(names))

    def test_no_alternative_is_another_terms_name(self):
        # Annars skulle ett svar kunna vara rätt på två olika frågor.
        names = {term["term"].lower() for term in TERMS}
        for term in TERMS:
            for alternative in term.get("alternativ", []):
                assert alternative.lower() not in names - {term["term"].lower()}, (term["term"], alternative)

    def test_every_part_of_the_course_has_terms(self):
        for first, last, title in bygg.PARTS:
            assert ova.terms_for_weeks(TERMS, first, last), title


class TestBuiltFiles:
    def test_markdown_is_up_to_date(self):
        assert bygg.MARKDOWN_FILE.read_text(encoding="utf-8") == bygg.build_markdown(TERMS), (
            "ORDLISTA.md är inte uppdaterad: kör python ordlista/bygg.py"
        )

    def test_html_is_up_to_date(self):
        assert bygg.HTML_FILE.read_text(encoding="utf-8") == bygg.build_html(TERMS), (
            "ordlista/index.html är inte uppdaterad: kör python ordlista/bygg.py"
        )

    def test_markdown_lists_every_term(self):
        markdown = bygg.MARKDOWN_FILE.read_text(encoding="utf-8")
        for term in TERMS:
            assert f"**{term['term'].replace('|', chr(92) + '|')}**" in markdown, term["term"]


class TestQuizLogic:
    @pytest.mark.parametrize("text, expected", [("3", (3, 3)), ("1-4", (1, 4)), ("19–24", (19, 24))])
    def test_parse_weeks(self, text, expected):
        assert ova.parse_weeks(text) == expected

    @pytest.mark.parametrize("text", ["", "fyra", "4-1", "1-2-3"])
    def test_parse_weeks_rejects_nonsense(self, text):
        with pytest.raises(ValueError):
            ova.parse_weeks(text)

    def test_terms_for_weeks(self):
        week_two = ova.terms_for_weeks(TERMS, 2, 2)
        assert week_two and all(term["vecka"] == 2 for term in week_two)

    def test_answers_ignore_case_and_extra_spaces(self):
        term = {"term": "linked list", "alternativ": []}
        assert ova.is_correct("  Linked   List ", term)
        assert not ova.is_correct("linkedlist", term)

    def test_alternatives_are_accepted(self):
        term = {"term": "dictionary", "alternativ": ["dict"]}
        assert ova.is_correct("DICT", term)

    def test_choices_contain_the_answer_once_among_four(self):
        rng = random.Random(1)
        term = TERMS[0]
        choices = ova.make_choices(term, TERMS, rng)
        assert len(choices) == 4
        assert choices.count(term) == 1
        assert len({choice["term"] for choice in choices}) == 4

    def test_run_quiz_scores_and_returns_missed_terms(self):
        questions = [
            {"term": "variable", "sv": "variabel", "forklaring": "Ett namn.", "vecka": 1},
            {"term": "loop", "sv": "loop", "forklaring": "Upprepning.", "vecka": 2},
        ]
        answers = iter(["Variable", "fel svar"])
        output = []
        missed = ova.run_quiz(questions, TERMS, "skriv", random.Random(0), lambda prompt: next(answers), output.append)
        assert [term["term"] for term in missed] == ["loop"]
        assert "\nResultat: 1 av 2 rätt." in output

    def test_run_quiz_multiple_choice(self):
        rng = random.Random(3)
        term = TERMS[5]
        choices = ova.make_choices(term, TERMS, random.Random(3))
        correct_letter = ova.CHOICE_LETTERS[choices.index(term)]
        missed = ova.run_quiz([term], TERMS, "flerval", rng, lambda prompt: correct_letter, lambda text: None)
        assert missed == []
