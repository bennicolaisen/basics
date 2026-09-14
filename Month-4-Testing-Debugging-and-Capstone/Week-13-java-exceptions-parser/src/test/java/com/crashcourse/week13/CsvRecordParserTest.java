package com.crashcourse.week13;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CsvRecordParserTest {

    @Test
    @DisplayName("A well-formed line parses into a CsvRecord with the expected fields")
    void parsesWellFormedLine() throws MalformedRecordException {
        CsvRecord record = CsvRecordParser.parseLine("Alice,30,alice@example.com,Engineering");

        assertEquals("Alice", record.name());
        assertEquals(30, record.age());
        assertEquals("alice@example.com", record.email());
        assertEquals("Engineering", record.department());
    }

    @Test
    @DisplayName("Whitespace around each field is trimmed")
    void trimsWhitespaceAroundFields() throws MalformedRecordException {
        CsvRecord record = CsvRecordParser.parseLine(" Bob , 25 , bob@example.com , Sales ");

        assertEquals("Bob", record.name());
        assertEquals("Sales", record.department());
    }

    @Test
    @DisplayName("Wrong column count names both the expected and the actual count")
    void wrongColumnCountIsNamedPrecisely() {
        MalformedRecordException ex = assertThrows(MalformedRecordException.class,
            () -> CsvRecordParser.parseLine("Alice,30,alice@example.com"));

        assertTrue(ex.getMessage().contains("4"), "should mention the expected column count");
        assertTrue(ex.getMessage().contains("found 3"), "should mention the actual column count");
    }

    @Test
    @DisplayName("A non-numeric age names the offending value, not just 'invalid line'")
    void nonNumericAgeIsNamedPrecisely() {
        MalformedRecordException ex = assertThrows(MalformedRecordException.class,
            () -> CsvRecordParser.parseLine("Alice,thirty,alice@example.com,Engineering"));

        assertTrue(ex.getMessage().contains("thirty"), "should quote the bad value");
        assertTrue(ex.getMessage().toLowerCase().contains("whole number"),
            "should say what was expected instead");
    }

    @Test
    @DisplayName("A negative age is rejected and the message says why")
    void negativeAgeIsNamedPrecisely() {
        MalformedRecordException ex = assertThrows(MalformedRecordException.class,
            () -> CsvRecordParser.parseLine("Alice,-5,alice@example.com,Engineering"));

        assertTrue(ex.getMessage().contains("-5"));
        assertTrue(ex.getMessage().toLowerCase().contains("negative"));
    }

    @Test
    @DisplayName("A blank name is rejected and the message names the field")
    void blankNameIsNamedPrecisely() {
        MalformedRecordException ex = assertThrows(MalformedRecordException.class,
            () -> CsvRecordParser.parseLine("   ,30,alice@example.com,Engineering"));

        assertTrue(ex.getMessage().toLowerCase().contains("name"));
        assertTrue(ex.getMessage().toLowerCase().contains("blank"));
    }

    @Test
    @DisplayName("An email missing '@' is rejected and the message quotes it")
    void invalidEmailIsNamedPrecisely() {
        MalformedRecordException ex = assertThrows(MalformedRecordException.class,
            () -> CsvRecordParser.parseLine("Alice,30,alice-example.com,Engineering"));

        assertTrue(ex.getMessage().contains("alice-example.com"));
        assertTrue(ex.getMessage().contains("@"));
    }

    @Test
    @DisplayName("An empty line is rejected rather than silently accepted")
    void emptyLineIsRejected() {
        assertThrows(MalformedRecordException.class, () -> CsvRecordParser.parseLine(""));
    }
}
