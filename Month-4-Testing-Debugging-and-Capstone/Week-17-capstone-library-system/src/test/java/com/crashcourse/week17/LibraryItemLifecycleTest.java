package com.crashcourse.week17;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Checkout/return mechanics shared by every LibraryItem, exercised via Book. */
class LibraryItemLifecycleTest {

    private Book book;
    private Member member;

    @BeforeEach
    void setUp() {
        book = new Book("B1", "Effective Java", "Joshua Bloch", "978-0134685991");
        member = new Member("MEM1", "Alice", 5);
    }

    @Test
    @DisplayName("checkOut marks the item unavailable, records the borrower, and sets a due date")
    void checkOutUpdatesState() throws ItemNotAvailableException {
        book.checkOut(member);

        assertFalse(book.isAvailable());
        assertEquals(member, book.currentBorrower());
        assertEquals(LocalDate.now().plusDays(book.loanPeriodDays()), book.dueDate());
    }

    @Test
    @DisplayName("checkOut on an already-checked-out item throws ItemNotAvailableException")
    void checkOutTwiceThrows() throws ItemNotAvailableException {
        book.checkOut(member);
        Member other = new Member("MEM2", "Bob", 5);

        assertThrows(ItemNotAvailableException.class, () -> book.checkOut(other));
    }

    @Test
    @DisplayName("returnItem clears availability, borrower, and due date")
    void returnItemClearsState() throws ItemNotAvailableException {
        book.checkOut(member);

        book.returnItem();

        assertTrue(book.isAvailable());
        assertNull(book.currentBorrower());
        assertNull(book.dueDate());
    }
}
