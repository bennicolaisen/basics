package com.crashcourse.week17;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class LibraryTest {

    private Library library;
    private Book book;
    private DVD dvd;
    private Magazine magazine;
    private Member alice;

    @BeforeEach
    void setUp() {
        library = new Library();
        book = new Book("B1", "Effective Java", "Joshua Bloch", "978-0134685991");
        dvd = new DVD("D1", "The Matrix", 136);
        magazine = new Magazine("M1", "National Geographic", 250);
        alice = new Member("MEM1", "Alice", 2);

        library.addItem(book);
        library.addItem(dvd);
        library.addItem(magazine);
        library.addMember(alice);
    }

    @Nested
    @DisplayName("checkOut - happy paths")
    class CheckOutHappyPaths {

        @Test
        @DisplayName("checking out a Book makes it unavailable and adds it to the member's items")
        void checksOutBook() throws Exception {
            LibraryItem checkedOut = library.checkOut("MEM1", "B1");

            assertEquals(book, checkedOut);
            assertFalse(book.isAvailable());
            assertTrue(alice.borrowedItems().contains(book));
        }

        @Test
        @DisplayName("checking out a DVD makes it unavailable and adds it to the member's items")
        void checksOutDvd() throws Exception {
            library.checkOut("MEM1", "D1");

            assertFalse(dvd.isAvailable());
            assertTrue(alice.borrowedItems().contains(dvd));
        }

        @Test
        @DisplayName("checking out a Magazine makes it unavailable and adds it to the member's items")
        void checksOutMagazine() throws Exception {
            library.checkOut("MEM1", "M1");

            assertFalse(magazine.isAvailable());
            assertTrue(alice.borrowedItems().contains(magazine));
        }
    }

    @Nested
    @DisplayName("checkOut - failure conditions")
    class CheckOutFailures {

        @Test
        @DisplayName("throws MemberNotFoundException for an unknown member id")
        void throwsForUnknownMember() {
            assertThrows(MemberNotFoundException.class, () -> library.checkOut("NO-SUCH-MEMBER", "B1"));
        }

        @Test
        @DisplayName("throws ItemNotAvailableException for an unknown item id")
        void throwsForUnknownItem() {
            assertThrows(ItemNotAvailableException.class, () -> library.checkOut("MEM1", "NO-SUCH-ITEM"));
        }

        @Test
        @DisplayName("throws ItemNotAvailableException when the item is already checked out")
        void throwsWhenAlreadyCheckedOut() throws Exception {
            Member bob = new Member("MEM2", "Bob", 2);
            library.addMember(bob);
            library.checkOut("MEM1", "B1");

            assertThrows(ItemNotAvailableException.class, () -> library.checkOut("MEM2", "B1"));
        }

        @Test
        @DisplayName("throws BorrowingLimitExceededException once the member's limit is reached")
        void throwsWhenLimitExceeded() throws Exception {
            library.checkOut("MEM1", "B1");
            library.checkOut("MEM1", "D1");

            assertThrows(BorrowingLimitExceededException.class, () -> library.checkOut("MEM1", "M1"));
        }
    }

    @Nested
    @DisplayName("returnItem")
    class ReturnItem {

        @Test
        @DisplayName("returning a checked-out item makes it available again and removes it from the member")
        void returnsCheckedOutItem() throws Exception {
            library.checkOut("MEM1", "B1");

            library.returnItem("MEM1", "B1");

            assertTrue(book.isAvailable());
            assertFalse(alice.borrowedItems().contains(book));
        }

        @Test
        @DisplayName("frees up room for another checkout once returned")
        void returnFreesUpBorrowingLimit() throws Exception {
            library.checkOut("MEM1", "B1");
            library.checkOut("MEM1", "D1");

            library.returnItem("MEM1", "B1");

            assertTrue(alice.hasReachedBorrowingLimit() == false);
            // Should not throw now that a slot has freed up.
            library.checkOut("MEM1", "M1");
        }

        @Test
        @DisplayName("throws MemberNotFoundException for an unknown member id")
        void throwsForUnknownMember() {
            assertThrows(MemberNotFoundException.class, () -> library.returnItem("NO-SUCH-MEMBER", "B1"));
        }

        @Test
        @DisplayName("throws IllegalStateException when the item was never checked out")
        void throwsWhenNotCheckedOut() {
            assertThrows(IllegalStateException.class, () -> library.returnItem("MEM1", "B1"));
        }
    }

    @Nested
    @DisplayName("overdueItems")
    class OverdueItems {

        @Test
        @DisplayName("an item checked out and now past its due date is reported overdue")
        void reportsOverdueItem() throws Exception {
            library.checkOut("MEM1", "B1"); // Book: 21-day loan period

            List<LibraryItem> overdue = library.overdueItems(LocalDate.now().plusDays(22));

            assertTrue(overdue.contains(book));
        }

        @Test
        @DisplayName("an item checked out but not yet due is not reported overdue")
        void doesNotReportItemNotYetDue() throws Exception {
            library.checkOut("MEM1", "B1");

            List<LibraryItem> overdue = library.overdueItems(LocalDate.now());

            assertFalse(overdue.contains(book));
        }

        @Test
        @DisplayName("an item that was never checked out is never reported overdue")
        void doesNotReportUncheckedOutItem() {
            List<LibraryItem> overdue = library.overdueItems(LocalDate.now().plusYears(1));

            assertFalse(overdue.contains(dvd));
        }
    }
}
