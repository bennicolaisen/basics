from text_analyzer.analyzer import (
    longest_words,
    tokenize,
    top_n_words,
    unique_words,
    word_frequencies,
)


class TestTokenize:
    def test_lowercases(self):
        assert tokenize("Hello WORLD") == ["hello", "world"]

    def test_strips_punctuation(self):
        assert tokenize("Hello, world! It's great.") == ["hello", "world", "its", "great"]

    def test_multiple_whitespace_and_newlines(self):
        assert tokenize("a   b\tc\nd") == ["a", "b", "c", "d"]

    def test_empty_string(self):
        assert tokenize("") == []

    def test_only_punctuation_yields_no_tokens(self):
        assert tokenize("!!! ??? ...") == []

    def test_mixed_case_and_punctuation_together(self):
        assert tokenize("Wow! Amazing... Right?") == ["wow", "amazing", "right"]


class TestWordFrequencies:
    def test_counts_correctly(self):
        assert word_frequencies(["a", "b", "a", "c", "a"]) == {"a": 3, "b": 1, "c": 1}

    def test_empty_list(self):
        assert word_frequencies([]) == {}

    def test_single_token(self):
        assert word_frequencies(["only"]) == {"only": 1}


class TestTopNWords:
    def test_sorted_by_count_descending(self):
        freqs = {"a": 1, "b": 3, "c": 2}
        assert top_n_words(freqs, 3) == [("b", 3), ("c", 2), ("a", 1)]

    def test_tie_break_is_alphabetical_ascending(self):
        freqs = {"zebra": 2, "apple": 2, "mango": 1}
        assert top_n_words(freqs, 3) == [("apple", 2), ("zebra", 2), ("mango", 1)]

    def test_n_limits_results(self):
        freqs = {"a": 5, "b": 4, "c": 3}
        assert top_n_words(freqs, 2) == [("a", 5), ("b", 4)]

    def test_n_larger_than_available_returns_all(self):
        assert top_n_words({"a": 1}, 5) == [("a", 1)]

    def test_empty_freqs(self):
        assert top_n_words({}, 3) == []


class TestUniqueWords:
    def test_removes_duplicates(self):
        assert unique_words(["a", "b", "a", "c"]) == {"a", "b", "c"}

    def test_empty_list(self):
        assert unique_words([]) == set()


class TestLongestWords:
    def test_sorted_by_length_descending(self):
        assert longest_words(["a", "bb", "ccc"], 3) == ["ccc", "bb", "a"]

    def test_tie_break_is_alphabetical_ascending(self):
        assert longest_words(["zz", "aa", "b"], 2) == ["aa", "zz"]

    def test_deduplicates_before_ranking(self):
        assert longest_words(["ab", "ab", "cd"], 2) == ["ab", "cd"]

    def test_n_limits_results(self):
        assert longest_words(["a", "bb", "ccc", "dddd"], 2) == ["dddd", "ccc"]
