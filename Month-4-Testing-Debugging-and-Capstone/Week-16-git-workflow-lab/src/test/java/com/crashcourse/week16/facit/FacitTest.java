package com.crashcourse.week16.facit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.time.Instant;
import org.junit.jupiter.api.Test;

/** Facit, steg 7: nya tester för taggen och för den sammanslagna toString. */
class FacitTest {

    private static final Instant WHEN = Instant.parse("2026-03-01T10:15:30Z");

    @Test
    void taggedConstructorStoresTheTag() {
        Note note = new Note(1, WHEN, "Buy milk", "shopping");
        assertEquals("shopping", note.tag());
        assertEquals("Buy milk", note.text());
    }

    @Test
    void threeArgumentConstructorStillWorksAndHasNoTag() {
        Note note = new Note(2, WHEN, "Call mum");
        assertNull(note.tag());
    }

    @Test
    void toStringWithoutTagHasNoTimestamp() {
        assertEquals("[2] Call mum", new Note(2, WHEN, "Call mum").toString());
    }

    @Test
    void toStringWithTagShowsTagButNoTimestamp() {
        assertEquals("[1] (shopping) Buy milk", new Note(1, WHEN, "Buy milk", "shopping").toString());
    }

    @Test
    void taggedConstructorValidatesLikeTheOldOne() {
        assertThrows(IllegalArgumentException.class, () -> new Note(0, WHEN, "x", "tag"));
        assertThrows(IllegalArgumentException.class, () -> new Note(1, null, "x", "tag"));
        assertThrows(IllegalArgumentException.class, () -> new Note(1, WHEN, " ", "tag"));
        assertThrows(IllegalArgumentException.class, () -> new Note(1, WHEN, "a\nb", "tag"));
    }
}
