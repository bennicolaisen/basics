package com.crashcourse.week16;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.Instant;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class NoteTest {

    @Test
    @DisplayName("constructs successfully with valid fields")
    void constructsWithValidFields() {
        Instant now = Instant.now();
        Note note = new Note(1, now, "Buy milk");

        assertEquals(1, note.id());
        assertEquals(now, note.createdAt());
        assertEquals("Buy milk", note.text());
    }

    @Test
    @DisplayName("rejects a non-positive id")
    void rejectsNonPositiveId() {
        assertThrows(IllegalArgumentException.class, () -> new Note(0, Instant.now(), "text"));
        assertThrows(IllegalArgumentException.class, () -> new Note(-1, Instant.now(), "text"));
    }

    @Test
    @DisplayName("rejects blank text")
    void rejectsBlankText() {
        assertThrows(IllegalArgumentException.class, () -> new Note(1, Instant.now(), "   "));
    }

    @Test
    @DisplayName("rejects text containing a newline")
    void rejectsMultilineText() {
        assertThrows(IllegalArgumentException.class, () -> new Note(1, Instant.now(), "line one\nline two"));
    }
}
