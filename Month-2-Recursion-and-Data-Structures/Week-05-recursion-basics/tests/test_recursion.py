import pytest

from recursion_basics.recursion import (
    factorial,
    fibonacci,
    is_palindrome_recursive,
    power,
    reverse_string,
    sum_digits,
)


class TestFactorial:
    def test_base_case(self):
        assert factorial(0) == 1

    def test_small_values(self):
        assert factorial(1) == 1
        assert factorial(4) == 24
        assert factorial(5) == 120

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            factorial(-1)


class TestFibonacci:
    def test_base_cases(self):
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1

    def test_known_sequence(self):
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21]
        assert [fibonacci(n) for n in range(len(expected))] == expected

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            fibonacci(-3)


class TestSumDigits:
    def test_single_digit(self):
        assert sum_digits(7) == 7
        assert sum_digits(0) == 0

    def test_multiple_digits(self):
        assert sum_digits(123) == 6
        assert sum_digits(9999) == 36

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            sum_digits(-12)


class TestReverseString:
    def test_empty(self):
        assert reverse_string("") == ""

    def test_single_char(self):
        assert reverse_string("a") == "a"

    def test_word(self):
        assert reverse_string("hello") == "olleh"

    def test_palindrome_word(self):
        assert reverse_string("level") == "level"


class TestIsPalindromeRecursive:
    def test_empty_and_single(self):
        assert is_palindrome_recursive("") is True
        assert is_palindrome_recursive("a") is True

    def test_true_cases(self):
        assert is_palindrome_recursive("level") is True
        assert is_palindrome_recursive("racecar") is True

    def test_false_cases(self):
        assert is_palindrome_recursive("hello") is False
        assert is_palindrome_recursive("almost") is False

    def test_case_sensitive(self):
        assert is_palindrome_recursive("Level") is False


class TestPower:
    def test_base_case(self):
        assert power(5, 0) == 1
        assert power(0, 0) == 1

    def test_positive_exponent(self):
        assert power(2, 10) == 1024
        assert power(3, 3) == 27

    def test_float_base(self):
        assert power(1.5, 2) == pytest.approx(2.25)

    def test_negative_exponent_raises(self):
        with pytest.raises(ValueError):
            power(2, -1)
