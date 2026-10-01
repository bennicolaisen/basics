"""Tester för facit till "Prova själv" (facit/prova_sjalv.py)."""

import pytest

from facit import prova_sjalv as facit
from text_analyzer.analyzer import tokenize, word_frequencies


def test_1_keeps_punctuation_inside_words():
    assert facit.tokenize_keep_inner("Don't stop (now)!") == ["don't", "stop", "now"]


def test_1_drops_tokens_that_were_only_punctuation():
    assert facit.tokenize_keep_inner("Hej - du ...") == ["hej", "du"]


def test_1_differs_from_the_original_only_inside_words():
    assert tokenize("Don't stop") == ["dont", "stop"]


def test_2_bigrams():
    assert facit.bigrams(["a", "b", "c"]) == [("a", "b"), ("b", "c")]
    assert facit.bigrams(["a"]) == []


def test_2_most_common_bigram():
    tokens = tokenize("det regnar och det regnar och det snöar")
    assert facit.most_common_bigram(tokens) == ("det", "regnar")
    with pytest.raises(ValueError):
        facit.most_common_bigram(["ensam"])


def test_3_stopwords_are_left_out():
    frequencies = word_frequencies(tokenize("det regnar och det snöar och det blåser"))
    assert facit.top_n_words_without(frequencies, 2, {"det", "och"}) == [("blåser", 1), ("regnar", 1)]


def test_4_average_counts_repeated_words():
    # "a" tre gånger och "bbb" en gång: (1 + 1 + 1 + 3) / 4 = 1.5. Räknat på
    # unika ord hade svaret blivit (1 + 3) / 2 = 2.0.
    assert facit.average_word_length(["a", "a", "a", "bbb"]) == pytest.approx(1.5)
    with pytest.raises(ValueError):
        facit.average_word_length([])


@pytest.mark.parametrize("n", [0, -1])
def test_5_n_must_be_positive(n):
    with pytest.raises(ValueError):
        facit.top_n_words({"a": 1}, n)
    with pytest.raises(ValueError):
        facit.longest_words(["a"], n)


def test_5_valid_n_still_works():
    assert facit.top_n_words({"a": 2, "b": 1}, 1) == [("a", 2)]
    assert facit.longest_words(["kort", "längre"], 1) == ["längre"]
