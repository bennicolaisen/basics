package com.crashcourse.week17.facit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.LocalDate;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

class FacitTest {

    private Library library;
    private Book book;
    private DVD dvd;
    private Magazine magazine;
    private AudioBook audioBook;
    private Member alice;
    private Member bob;
    private Member carol;

    @BeforeEach
    void setUp() {
        library = new Library();
        book = new Book("B1", "Effective Java", "Joshua Bloch", "978-0134685991");
        dvd = new DVD("D1", "The Matrix", 136);
        magazine = new Magazine("M1", "National Geographic", 250);
        audioBook = new AudioBook("A1", "Dune", "Scott Brick", 1260);
        alice = new Member("MEM1", "Alice", 3);
        bob = new Member("MEM2", "Bob", 3);
        carol = new Member("MEM3", "Carol", 3);
        for (LibraryItem item : List.of(book, dvd, magazine, audioBook)) {
            library.addItem(item);
        }
        for (Member member : List.of(alice, bob, carol)) {
            library.addMember(member);
        }
    }

    @Nested
    @DisplayName("Uppgift 1: AudioBook")
    class AudioBookTests {

        @Test
        void hasNarratorAndOwnLoanPeriod() {
            assertEquals("Scott Brick", audioBook.narrator());
            assertEquals(14, audioBook.loanPeriodDays());
        }

        @Test
        void canBeCheckedOutAndReturnedWithoutAnyChangeToLibrary() throws Exception {
            library.checkOut("MEM1", "A1");
            assertFalse(audioBook.isAvailable());
            assertEquals(LocalDate.now().plusDays(14), audioBook.dueDate());
            library.returnItem("MEM1", "A1");
            assertTrue(audioBook.isAvailable());
        }

        @Test
        void validatesItsOwnFields() {
            assertThrows(IllegalArgumentException.class, () -> new AudioBook("A2", "T", " ", 10));
            assertThrows(IllegalArgumentException.class, () -> new AudioBook("A2", "T", "N", 0));
        }
    }

    @Nested
    @DisplayName("Uppgift 2: renew")
    class RenewTests {

        @Test
        void extendsDueDateByOneLoanPeriod() throws Exception {
            library.checkOut("MEM1", "B1");
            LocalDate before = book.dueDate();
            LocalDate after = library.renew("MEM1", "B1");
            assertEquals(before.plusDays(21), after);
            assertEquals(after, book.dueDate());
        }

        @Test
        void canRenewMoreThanOnce() throws Exception {
            library.checkOut("MEM1", "D1");
            LocalDate before = dvd.dueDate();
            library.renew("MEM1", "D1");
            library.renew("MEM1", "D1");
            assertEquals(before.plusDays(14), dvd.dueDate());
        }

        @Test
        void cannotRenewAnItemThatIsNotCheckedOut() {
            assertThrows(IllegalStateException.class, () -> library.renew("MEM1", "B1"));
        }

        @Test
        void cannotRenewSomeoneElsesLoan() throws Exception {
            library.checkOut("MEM1", "B1");
            assertThrows(IllegalStateException.class, () -> library.renew("MEM2", "B1"));
        }

        @Test
        void unknownMemberOrItem() {
            assertThrows(MemberNotFoundException.class, () -> library.renew("NOPE", "B1"));
            assertThrows(IllegalArgumentException.class, () -> library.renew("MEM1", "NOPE"));
        }

        @Test
        void cannotRenewWhenSomeoneIsWaiting() throws Exception {
            library.checkOut("MEM1", "B1");
            library.placeHold("MEM2", "B1");
            LocalDate before = book.dueDate();
            assertThrows(ItemNotAvailableException.class, () -> library.renew("MEM1", "B1"));
            assertEquals(before, book.dueDate());
        }
    }

    @Nested
    @DisplayName("Uppgift 3: holds")
    class HoldTests {

        @Test
        void returnedItemIsReservedForFirstInQueue() throws Exception {
            library.checkOut("MEM1", "B1");
            library.placeHold("MEM2", "B1");
            library.placeHold("MEM3", "B1");
            assertEquals(List.of(bob, carol), library.holdsFor("B1").waiting());

            library.returnItem("MEM1", "B1");

            assertTrue(book.isAvailable());
            assertSame(bob, library.holdsFor("B1").reservedFor());
            assertEquals(List.of(carol), library.holdsFor("B1").waiting());
        }

        @Test
        void othersCannotTakeAReservedItem() throws Exception {
            library.checkOut("MEM1", "B1");
            library.placeHold("MEM2", "B1");
            library.returnItem("MEM1", "B1");

            assertThrows(ItemNotAvailableException.class, () -> library.checkOut("MEM3", "B1"));
            assertThrows(ItemNotAvailableException.class, () -> library.checkOut("MEM1", "B1"));

            library.checkOut("MEM2", "B1");
            assertSame(bob, book.currentBorrower());
            assertNull(library.holdsFor("B1").reservedFor());
        }

        @Test
        void queueMovesOnAfterEachReturn() throws Exception {
            library.checkOut("MEM1", "B1");
            library.placeHold("MEM2", "B1");
            library.placeHold("MEM3", "B1");
            library.returnItem("MEM1", "B1");
            library.checkOut("MEM2", "B1");
            library.returnItem("MEM2", "B1");
            assertSame(carol, library.holdsFor("B1").reservedFor());
            library.checkOut("MEM3", "B1");
            library.returnItem("MEM3", "B1");
            assertNull(library.holdsFor("B1").reservedFor());
            library.checkOut("MEM1", "B1");
        }

        @Test
        void withoutHoldsAReturnedItemGoesBackToEveryone() throws Exception {
            library.checkOut("MEM1", "B1");
            library.returnItem("MEM1", "B1");
            library.checkOut("MEM3", "B1");
            assertSame(carol, book.currentBorrower());
        }

        @Test
        void cannotHoldAnAvailableItem() {
            assertThrows(IllegalStateException.class, () -> library.placeHold("MEM1", "B1"));
        }

        @Test
        void canHoldAnItemReservedForSomeoneElse() throws Exception {
            library.checkOut("MEM1", "B1");
            library.placeHold("MEM2", "B1");
            library.returnItem("MEM1", "B1");
            library.placeHold("MEM3", "B1");
            assertEquals(List.of(carol), library.holdsFor("B1").waiting());
        }

        @Test
        void cannotHoldTwiceOrHoldYourOwnLoan() throws Exception {
            library.checkOut("MEM1", "B1");
            library.placeHold("MEM2", "B1");
            assertThrows(IllegalStateException.class, () -> library.placeHold("MEM2", "B1"));
            assertThrows(IllegalStateException.class, () -> library.placeHold("MEM1", "B1"));
        }

        @Test
        void reservedMemberStillRespectsBorrowingLimit() throws Exception {
            Member dave = new Member("MEM4", "Dave", 1);
            library.addMember(dave);
            library.checkOut("MEM1", "B1");
            library.placeHold("MEM4", "B1");
            library.checkOut("MEM4", "D1");
            library.returnItem("MEM1", "B1");
            assertThrows(BorrowingLimitExceededException.class, () -> library.checkOut("MEM4", "B1"));
            assertSame(dave, library.holdsFor("B1").reservedFor());
        }
    }

    @Nested
    @DisplayName("Uppgift 4: overdueItemsForMember")
    class OverdueTests {

        @Test
        void onlyThatMembersOverdueItems() throws Exception {
            library.checkOut("MEM1", "B1");  // 21 dagar
            library.checkOut("MEM1", "D1");  // 7 dagar
            library.checkOut("MEM2", "M1");  // 14 dagar
            LocalDate inTenDays = LocalDate.now().plusDays(10);

            assertEquals(List.of(dvd), library.overdueItemsForMember("MEM1", inTenDays));
            assertEquals(List.of(), library.overdueItemsForMember("MEM2", inTenDays));
            assertEquals(2, library.overdueItemsForMember("MEM1", LocalDate.now().plusDays(30)).size());
        }

        @Test
        void dueTodayIsNotOverdue() throws Exception {
            library.checkOut("MEM1", "D1");
            assertTrue(library.overdueItemsForMember("MEM1", dvd.dueDate()).isEmpty());
        }

        @Test
        void unknownMemberThrows() {
            assertThrows(MemberNotFoundException.class,
                () -> library.overdueItemsForMember("NOPE", LocalDate.now()));
        }
    }

    @Nested
    @DisplayName("Uppgift 5: gräns per sort")
    class PerTypeLimitTests {

        @BeforeEach
        void useAPolicy() {
            library = new Library(new BorrowingPolicy().limit(Book.class, 3).limit(DVD.class, 1));
            library.addItem(book);
            library.addItem(dvd);
            library.addItem(new DVD("D2", "Alien", 117));
            library.addItem(new Book("B2", "Clean Code", "Robert C. Martin", "978-0132350884"));
            library.addItem(audioBook);
            library.addMember(new Member("BIG", "Big Reader", 10));
        }

        @Test
        void secondDvdIsRefused() throws Exception {
            library.checkOut("BIG", "D1");
            BorrowingLimitExceededException e = assertThrows(BorrowingLimitExceededException.class,
                () -> library.checkOut("BIG", "D2"));
            assertTrue(e.getMessage().contains("1 DVD"));
        }

        @Test
        void otherTypesAreCountedSeparately() throws Exception {
            library.checkOut("BIG", "D1");
            library.checkOut("BIG", "B1");
            library.checkOut("BIG", "B2");
            library.checkOut("BIG", "A1");  // ingen egen gräns för AudioBook
            assertEquals(4, library.findMember("BIG").borrowedItems().size());
        }

        @Test
        void returningFreesUpTheTypeLimit() throws Exception {
            library.checkOut("BIG", "D1");
            library.returnItem("BIG", "D1");
            library.checkOut("BIG", "D2");
        }

        @Test
        void totalLimitStillApplies() throws Exception {
            library.addMember(new Member("SMALL", "Small Reader", 1));
            library.checkOut("SMALL", "B1");
            assertThrows(BorrowingLimitExceededException.class, () -> library.checkOut("SMALL", "D1"));
        }

        @Test
        void policyRejectsNonsense() {
            assertThrows(IllegalArgumentException.class, () -> new BorrowingPolicy().limit(DVD.class, 0));
        }
    }

    @Test
    @DisplayName("Rättad bugg: man kan inte lämna tillbaka någon annans lån")
    void cannotReturnSomeoneElsesLoan() throws Exception {
        library.checkOut("MEM1", "B1");
        assertThrows(IllegalStateException.class, () -> library.returnItem("MEM2", "B1"));
        assertFalse(book.isAvailable());
        assertTrue(alice.borrowedItems().contains(book));
    }
}
