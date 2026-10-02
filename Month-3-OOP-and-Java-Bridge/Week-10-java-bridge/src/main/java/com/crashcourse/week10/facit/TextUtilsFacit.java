package com.crashcourse.week10.facit;

import java.util.regex.Pattern;

/** Facit, uppgift 2 och 3: longestWord och en wordCount med egen avgränsare. Se FACIT.md. */
public final class TextUtilsFacit {

    private TextUtilsFacit() {
    }

    /**
     * Det längsta whitespace-separerade ordet i {@code text}.
     *
     * <p>Vid lika längd vinner ordet som kommer först i texten. En tom eller
     * blank text ger en tom sträng.
     */
    public static String longestWord(String text) {
        if (text == null) {
            throw new IllegalArgumentException("text must not be null");
        }
        String longest = "";
        for (String word : text.trim().split("\\s+")) {
            if (word.length() > longest.length()) {
                longest = word;
            }
        }
        return longest;
    }

    /**
     * Antalet delar mellan {@code delimiter}, där tomma delar inte räknas:
     * {@code wordCount("a,,b", ",")} är 2.
     *
     * <p>Avgränsaren tolkas bokstavligt, inte som ett reguljärt uttryck, så
     * {@code "."} betyder en punkt och inte "vilket tecken som helst".
     */
    public static int wordCount(String text, String delimiter) {
        if (text == null || delimiter == null || delimiter.isEmpty()) {
            throw new IllegalArgumentException("text and delimiter must be non-empty");
        }
        int count = 0;
        for (String part : text.split(Pattern.quote(delimiter))) {
            if (!part.isBlank()) {
                count++;
            }
        }
        return count;
    }
}
