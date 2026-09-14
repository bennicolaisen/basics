package com.crashcourse.week17;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Validation and type-specific behavior for each concrete LibraryItem. */
class LibraryItemTypesTest {

    @Nested
    @DisplayName("Book")
    class BookTests {

        @Test
        @DisplayName("constructs with valid fields and a 21-day loan period")
        void constructsValidBook() {
            Book book = new Book("B1", "Effective Java", "Joshua Bloch", "978-0134685991");

            assertEquals("B1", book.id());
            assertEquals("Effective Java", book.title());
            assertEquals("Joshua Bloch", book.author());
            assertEquals("978-0134685991", book.isbn());
            assertEquals(21, book.loanPeriodDays());
            assertTrue(book.isAvailable());
        }

        @Test
        @DisplayName("rejects a blank author")
        void rejectsBlankAuthor() {
            assertThrows(IllegalArgumentException.class,
                () -> new Book("B1", "Effective Java", "  ", "978-0134685991"));
        }

        @Test
        @DisplayName("rejects a blank ISBN")
        void rejectsBlankIsbn() {
            assertThrows(IllegalArgumentException.class,
                () -> new Book("B1", "Effective Java", "Joshua Bloch", ""));
        }
    }

    @Nested
    @DisplayName("DVD")
    class DvdTests {

        @Test
        @DisplayName("constructs with valid fields and a 7-day loan period")
        void constructsValidDvd() {
            DVD dvd = new DVD("D1", "The Matrix", 136);

            assertEquals("D1", dvd.id());
            assertEquals("The Matrix", dvd.title());
            assertEquals(136, dvd.runtimeMinutes());
            assertEquals(7, dvd.loanPeriodDays());
        }

        @Test
        @DisplayName("rejects a non-positive runtime")
        void rejectsNonPositiveRuntime() {
            assertThrows(IllegalArgumentException.class, () -> new DVD("D1", "The Matrix", 0));
            assertThrows(IllegalArgumentException.class, () -> new DVD("D1", "The Matrix", -5));
        }
    }

    @Nested
    @DisplayName("Magazine")
    class MagazineTests {

        @Test
        @DisplayName("constructs with valid fields and a 14-day loan period")
        void constructsValidMagazine() {
            Magazine magazine = new Magazine("M1", "National Geographic", 250);

            assertEquals("M1", magazine.id());
            assertEquals("National Geographic", magazine.title());
            assertEquals(250, magazine.issueNumber());
            assertEquals(14, magazine.loanPeriodDays());
        }

        @Test
        @DisplayName("rejects a non-positive issue number")
        void rejectsNonPositiveIssueNumber() {
            assertThrows(IllegalArgumentException.class, () -> new Magazine("M1", "Nat Geo", 0));
        }
    }

    @Nested
    @DisplayName("Common LibraryItem validation")
    class CommonValidationTests {

        @Test
        @DisplayName("rejects a blank id regardless of concrete type")
        void rejectsBlankId() {
            assertThrows(IllegalArgumentException.class,
                () -> new Book("  ", "Title", "Author", "ISBN"));
        }

        @Test
        @DisplayName("rejects a blank title regardless of concrete type")
        void rejectsBlankTitle() {
            assertThrows(IllegalArgumentException.class,
                () -> new DVD("D1", " ", 100));
        }
    }
}
