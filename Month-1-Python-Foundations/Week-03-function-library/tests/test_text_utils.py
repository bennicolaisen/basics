from function_library.text_utils import is_palindrome, word_count


class TestWordCount:
    def test_typical_sentence(self):
        assert word_count("the quick brown fox") == 4

    def test_empty_string(self):
        assert word_count("") == 0

    def test_only_whitespace(self):
        assert word_count("   ") == 0

    def test_extra_internal_whitespace(self):
        assert word_count("a   b\tc\nd") == 4

    def test_leading_and_trailing_whitespace(self):
        assert word_count("  hello world  ") == 2

    def test_single_word(self):
        assert word_count("hello") == 1


class TestIsPalindrome:
    def test_simple_palindrome(self):
        assert is_palindrome("racecar") is True

    def test_simple_non_palindrome(self):
        assert is_palindrome("hello") is False

    def test_default_ignores_case_and_spaces(self):
        assert is_palindrome("A man a plan a canal Panama") is True

    def test_case_sensitive_when_disabled(self):
        assert is_palindrome("Racecar", ignore_case=False) is False

    def test_space_sensitive_when_disabled(self):
        assert is_palindrome("race car", ignore_spaces=False) is False

    def test_empty_string_is_palindrome(self):
        assert is_palindrome("") is True

    def test_single_character(self):
        assert is_palindrome("x") is True

    def test_both_flags_disabled_exact_match_required(self):
        assert is_palindrome("Never Odd Or Even", ignore_case=False, ignore_spaces=False) is False
