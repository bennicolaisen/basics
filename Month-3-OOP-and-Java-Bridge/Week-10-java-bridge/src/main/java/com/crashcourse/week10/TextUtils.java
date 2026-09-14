package com.crashcourse.week10;

/**
 * Static text utilities — a Java port of small text-analysis helpers from
 * Month 1, Week 3's function library.
 */
public final class TextUtils {

    private TextUtils() {
    }

    /**
     * Counts whitespace-separated words in {@code text}. An empty or
     * blank string has zero words.
     */
    public static int wordCount(String text) {
        if (text == null) {
            throw new IllegalArgumentException("text must not be null");
        }
        String trimmed = text.trim();
        if (trimmed.isEmpty()) {
            return 0;
        }
        return trimmed.split("\\s+").length;
    }

    /**
     * Case-sensitive palindrome check, ignoring nothing — exact
     * character-by-character comparison against its own reverse.
     */
    public static boolean isPalindrome(String text) {
        return isPalindrome(text, false);
    }

    /**
     * Palindrome check with an explicit choice of whether case is ignored.
     * Overloading {@link #isPalindrome(String)} for the common case and
     * this two-argument form for the configurable case is a small, real
     * example of Java method overloading: two methods, same name,
     * different parameter lists, resolved at compile time by the
     * arguments you pass.
     */
    public static boolean isPalindrome(String text, boolean ignoreCase) {
        if (text == null) {
            throw new IllegalArgumentException("text must not be null");
        }
        String candidate = ignoreCase ? text.toLowerCase() : text;
        String reversed = new StringBuilder(candidate).reverse().toString();
        return candidate.equals(reversed);
    }
}
