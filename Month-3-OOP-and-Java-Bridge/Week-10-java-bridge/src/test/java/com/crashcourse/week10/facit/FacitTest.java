package com.crashcourse.week10.facit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.Locale;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class FacitTest {

    private Locale originalLocale;

    @BeforeEach
    void useDotAsDecimalSeparator() {
        // String.format follows the machine's locale; a Swedish locale would print "21,5".
        originalLocale = Locale.getDefault();
        Locale.setDefault(Locale.US);
    }

    @AfterEach
    void restoreLocale() {
        Locale.setDefault(originalLocale);
    }

    @Test
    void absoluteZeroInBothDirections() {
        assertEquals(0.0, ConvertersFacit.fahrenheitToKelvin(-459.67), 1e-9);
        assertEquals(-459.67, ConvertersFacit.kelvinToFahrenheit(0), 1e-9);
    }

    @Test
    void freezingPoint() {
        assertEquals(273.15, ConvertersFacit.fahrenheitToKelvin(32), 1e-9);
    }

    @Test
    void roundTrip() {
        assertEquals(300.0, ConvertersFacit.fahrenheitToKelvin(ConvertersFacit.kelvinToFahrenheit(300.0)), 1e-9);
    }

    @Test
    void belowAbsoluteZeroIsRejected() {
        assertThrows(IllegalArgumentException.class, () -> ConvertersFacit.kelvinToFahrenheit(-1));
        assertThrows(IllegalArgumentException.class, () -> ConvertersFacit.fahrenheitToKelvin(-500));
    }

    @Test
    void longestWordPicksTheFirstOnATie() {
        assertEquals("quick", TextUtilsFacit.longestWord("the quick brown fox"));
        assertEquals("aa", TextUtilsFacit.longestWord("aa bb c"));
    }

    @Test
    void longestWordOfBlankTextIsEmpty() {
        assertEquals("", TextUtilsFacit.longestWord("   "));
    }

    @Test
    void longestWordRejectsNull() {
        assertThrows(IllegalArgumentException.class, () -> TextUtilsFacit.longestWord(null));
    }

    @Test
    void wordCountWithCustomDelimiterSkipsEmptyParts() {
        assertEquals(3, TextUtilsFacit.wordCount("Oslo,Umeå,,Visby", ","));
        assertEquals(0, TextUtilsFacit.wordCount(",,", ","));
    }

    @Test
    void wordCountDelimiterIsLiteralNotARegex() {
        assertEquals(3, TextUtilsFacit.wordCount("a.b.c", "."));
    }

    @Test
    void wordCountRejectsEmptyDelimiter() {
        assertThrows(IllegalArgumentException.class, () -> TextUtilsFacit.wordCount("a", ""));
    }

    @Test
    void mainWithArgsHandlesAllThreeCases() {
        assertEquals("21.5 C is 70.7 F", MainWithArgs.describe(new String[] {"21.5"}));
        assertEquals("Usage: MainWithArgs <degrees Celsius>", MainWithArgs.describe(new String[0]));
        assertEquals("Not a number: varmt", MainWithArgs.describe(new String[] {"varmt"}));
    }
}
