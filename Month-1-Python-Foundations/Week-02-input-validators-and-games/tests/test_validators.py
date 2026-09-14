import pytest

from validators_and_games.validators import (
    is_strong_password,
    is_valid_username,
    parse_int_in_range,
)


class TestIsValidUsername:
    def test_typical_valid(self):
        assert is_valid_username("alice_99") is True

    def test_empty_string(self):
        assert is_valid_username("") is False

    def test_too_short_two_chars(self):
        assert is_valid_username("ab") is False

    def test_exactly_min_length_three(self):
        assert is_valid_username("abc") is True

    def test_exactly_max_length_twenty(self):
        assert is_valid_username("a" * 20) is True

    def test_one_over_max_length(self):
        assert is_valid_username("a" * 21) is False

    def test_starts_with_digit(self):
        assert is_valid_username("1abc") is False

    def test_starts_with_underscore(self):
        assert is_valid_username("_abc") is False

    def test_contains_space(self):
        assert is_valid_username("ab cde") is False

    def test_contains_hyphen(self):
        assert is_valid_username("ab-cde") is False

    def test_all_letters(self):
        assert is_valid_username("Charlie") is True

    def test_letters_digits_underscore_mix(self):
        assert is_valid_username("Bob_the_2nd") is True


class TestIsStrongPassword:
    def test_typical_strong(self):
        assert is_strong_password("Str0ng!Pw") is True

    def test_empty_string(self):
        assert is_strong_password("") is False

    def test_exactly_seven_chars_too_short(self):
        assert is_strong_password("Ab1!ab1") is False  # 7 chars

    def test_exactly_eight_chars_valid(self):
        assert is_strong_password("Ab1!abcd") is True  # 8 chars

    def test_missing_uppercase(self):
        assert is_strong_password("weak1234!") is False

    def test_missing_lowercase(self):
        assert is_strong_password("WEAK1234!") is False

    def test_missing_digit(self):
        assert is_strong_password("WeakPass!") is False

    def test_missing_symbol(self):
        assert is_strong_password("WeakPass1") is False

    def test_only_letters(self):
        assert is_strong_password("OnlyLetters") is False


class TestParseIntInRange:
    def test_typical_in_range(self):
        assert parse_int_in_range("5", 1, 10) == 5

    def test_lower_boundary_inclusive(self):
        assert parse_int_in_range("1", 1, 10) == 1

    def test_upper_boundary_inclusive(self):
        assert parse_int_in_range("10", 1, 10) == 10

    def test_one_below_lower_bound_raises(self):
        with pytest.raises(ValueError):
            parse_int_in_range("0", 1, 10)

    def test_one_above_upper_bound_raises(self):
        with pytest.raises(ValueError):
            parse_int_in_range("11", 1, 10)

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            parse_int_in_range("", 1, 10)

    def test_non_numeric_raises(self):
        with pytest.raises(ValueError):
            parse_int_in_range("abc", 1, 10)

    def test_float_string_raises(self):
        with pytest.raises(ValueError):
            parse_int_in_range("5.5", 1, 10)

    def test_negative_range(self):
        assert parse_int_in_range("-3", -10, -1) == -3

    def test_whitespace_padded_is_accepted(self):
        # int() itself tolerates surrounding whitespace; this documents
        # and locks in that inherited behaviour rather than leaving it
        # as an accident.
        assert parse_int_in_range("  7  ", 1, 10) == 7
