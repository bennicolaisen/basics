package com.crashcourse.week10;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class TextUtilsTest {

    @Test
    void wordCountCountsWhitespaceSeparatedWords() {
        assertEquals(9, TextUtils.wordCount("the quick brown fox jumps over the lazy dog"));
    }

    @Test
    void wordCountHandlesExtraWhitespace() {
        assertEquals(2, TextUtils.wordCount("  hello    world  "));
    }

    @Test
    void wordCountEmptyStringIsZero() {
        assertEquals(0, TextUtils.wordCount(""));
        assertEquals(0, TextUtils.wordCount("   "));
    }

    @Test
    void wordCountNullThrows() {
        assertThrows(IllegalArgumentException.class, () -> TextUtils.wordCount(null));
    }

    @Test
    void isPalindromeTrueForExactPalindrome() {
        assertTrue(TextUtils.isPalindrome("racecar"));
    }

    @Test
    void isPalindromeFalseForNonPalindrome() {
        assertFalse(TextUtils.isPalindrome("hello"));
    }

    @Test
    void isPalindromeCaseSensitiveByDefault() {
        assertFalse(TextUtils.isPalindrome("Racecar"));
    }

    @Test
    void isPalindromeIgnoreCaseOverload() {
        assertTrue(TextUtils.isPalindrome("Racecar", true));
    }

    @Test
    void isPalindromeEmptyStringIsTrue() {
        assertTrue(TextUtils.isPalindrome(""));
    }

    @Test
    void isPalindromeNullThrows() {
        assertThrows(IllegalArgumentException.class, () -> TextUtils.isPalindrome(null));
    }
}
