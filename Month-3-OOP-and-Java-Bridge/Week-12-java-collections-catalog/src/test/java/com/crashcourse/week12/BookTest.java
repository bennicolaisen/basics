package com.crashcourse.week12;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.HashSet;
import java.util.Set;
import java.util.TreeSet;
import org.junit.jupiter.api.Test;

class BookTest {

    @Test
    void equalsIsBasedOnIsbnAlone() {
        Book a = new Book("Dune", "Frank Herbert", "111", 1965);
        Book b = new Book("Dune (different printing)", "F. Herbert", "111", 1990);
        assertEquals(a, b, "same ISBN should make two Book instances equal regardless of other fields");
    }

    @Test
    void differentIsbnMeansNotEqual() {
        Book a = new Book("Dune", "Frank Herbert", "111", 1965);
        Book b = new Book("Dune", "Frank Herbert", "222", 1965);
        assertNotEquals(a, b);
    }

    @Test
    void equalBooksHaveEqualHashCodes() {
        Book a = new Book("Dune", "Frank Herbert", "111", 1965);
        Book b = new Book("Dune (different printing)", "F. Herbert", "111", 1990);
        assertEquals(a.hashCode(), b.hashCode());
    }

    @Test
    void equalBooksAreInterchangeableAsSetMembers() {
        Book a = new Book("Dune", "Frank Herbert", "111", 1965);
        Book b = new Book("Dune (different printing)", "F. Herbert", "111", 1990);

        Set<Book> set = new HashSet<>();
        set.add(a);
        assertTrue(set.contains(b), "a HashSet should treat equal-ISBN books as the same element");

        set.add(b);
        assertEquals(1, set.size(), "adding an equal book should not grow the set");
    }

    @Test
    void naturalOrderIsByTitle() {
        Book zebra = new Book("Zebra Stories", "Author A", "111", 2000);
        Book apple = new Book("Apple Tales", "Author B", "222", 2000);
        assertTrue(apple.compareTo(zebra) < 0);
        assertTrue(zebra.compareTo(apple) > 0);
    }

    @Test
    void naturalOrderWorksInATreeSet() {
        TreeSet<Book> sorted = new TreeSet<>();
        sorted.add(new Book("Zebra Stories", "A", "1", 2000));
        sorted.add(new Book("Apple Tales", "B", "2", 2000));
        sorted.add(new Book("Mango Days", "C", "3", 2000));

        assertEquals("Apple Tales", sorted.first().getTitle());
        assertEquals("Zebra Stories", sorted.last().getTitle());
    }

    @Test
    void blankTitleRejected() {
        assertThrows(IllegalArgumentException.class, () -> new Book("", "Author", "111", 2000));
    }

    @Test
    void nonPositiveYearRejected() {
        assertThrows(IllegalArgumentException.class, () -> new Book("Title", "Author", "111", 0));
    }
}
