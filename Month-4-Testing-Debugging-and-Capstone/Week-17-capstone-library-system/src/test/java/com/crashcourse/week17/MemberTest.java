package com.crashcourse.week17;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MemberTest {

    private Member member;

    @BeforeEach
    void setUp() {
        member = new Member("MEM1", "Alice", 2);
    }

    @Test
    @DisplayName("constructs successfully with valid fields")
    void constructsWithValidFields() {
        assertEquals("MEM1", member.id());
        assertEquals("Alice", member.name());
        assertEquals(2, member.borrowingLimit());
        assertTrue(member.borrowedItems().isEmpty());
    }

    @Test
    @DisplayName("rejects a blank id")
    void rejectsBlankId() {
        assertThrows(IllegalArgumentException.class, () -> new Member(" ", "Alice", 2));
    }

    @Test
    @DisplayName("rejects a blank name")
    void rejectsBlankName() {
        assertThrows(IllegalArgumentException.class, () -> new Member("MEM1", "", 2));
    }

    @Test
    @DisplayName("rejects a non-positive borrowing limit")
    void rejectsNonPositiveLimit() {
        assertThrows(IllegalArgumentException.class, () -> new Member("MEM1", "Alice", 0));
    }

    @Test
    @DisplayName("has not reached the limit below it, and has reached it at it")
    void tracksBorrowingLimit() {
        Book book1 = new Book("B1", "Book One", "Author", "ISBN1");
        Book book2 = new Book("B2", "Book Two", "Author", "ISBN2");

        assertFalse(member.hasReachedBorrowingLimit());

        member.addBorrowedItem(book1);
        assertFalse(member.hasReachedBorrowingLimit());

        member.addBorrowedItem(book2);
        assertTrue(member.hasReachedBorrowingLimit());

        member.removeBorrowedItem(book1);
        assertFalse(member.hasReachedBorrowingLimit());
    }
}
