package com.crashcourse.week12.facit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class FacitTest {

    private final Book dune = new Book("Dune", "Frank Herbert", "111", 1965);
    private final Book hobbit = new Book("The Hobbit", "J.R.R. Tolkien", "222", 1937);
    private final Book foundation = new Book("Foundation", "Isaac Asimov", "333", 1951);
    private final Book robots = new Book("I, Robot", "Isaac Asimov", "444", 1950);
    private final Book messiah = new Book("Dune Messiah", "Frank Herbert", "555", 1969);

    private Library library;

    @BeforeEach
    void fillLibrary() throws DuplicateIsbnException {
        library = new Library();
        for (Book book : List.of(dune, hobbit, foundation, robots, messiah)) {
            library.addBook(book);
        }
    }

    // Uppgift 1

    @Test
    void yearRangeIncludesBothBounds() {
        assertEquals(List.of(robots, foundation), library.findByYearRange(1950, 1951));
    }

    @Test
    void yearRangeWithSameFromAndToFindsThatYear() {
        assertEquals(List.of(dune), library.findByYearRange(1965, 1965));
    }

    @Test
    void yearRangeWithNoMatchesIsEmpty() {
        assertTrue(library.findByYearRange(2000, 2020).isEmpty());
    }

    @Test
    void yearRangeBackwardsThrows() {
        assertThrows(IllegalArgumentException.class, () -> library.findByYearRange(1960, 1950));
    }

    // Uppgift 2

    @Test
    void sortedByAuthorThenTitle() {
        // Frank Herbert: Dune, Dune Messiah. Isaac Asimov: Foundation, I, Robot.
        assertEquals(List.of(dune, messiah, foundation, robots, hobbit),
                library.booksSortedByAuthorThenTitle());
    }

    // Uppgift 3

    @Test
    void copiesOfTheSameIsbnAreCounted() {
        CopiesLibrary copies = new CopiesLibrary();
        copies.addBook(dune);
        copies.addBook(new Book("Dune", "Frank Herbert", "111", 1965));
        copies.addBook(new Book("Dune", "Frank Herbert", "111", 1965));
        copies.addBook(hobbit);
        assertEquals(3, copies.copiesOf("111"));
        assertEquals(4, copies.size());
        assertEquals(2, copies.titleCount());
    }

    @Test
    void sameIsbnWithDifferentBookIsRejected() {
        CopiesLibrary copies = new CopiesLibrary();
        copies.addBook(dune);
        Book impostor = new Book("Dune Messiah", "Frank Herbert", "111", 1969);
        assertThrows(IllegalArgumentException.class, () -> copies.addBook(impostor));
        assertEquals(1, copies.copiesOf("111"));
    }

    @Test
    void removingTheLastCopyRemovesTheIsbn() {
        CopiesLibrary copies = new CopiesLibrary();
        copies.addBook(dune);
        copies.addBook(new Book("Dune", "Frank Herbert", "111", 1965));
        assertTrue(copies.removeBook("111"));
        assertEquals(1, copies.copiesOf("111"));
        assertTrue(copies.removeBook("111"));
        assertEquals(0, copies.copiesOf("111"));
        assertNull(copies.findByIsbn("111"));
        assertEquals(0, copies.titleCount());
        assertFalse(copies.removeBook("111"));
    }

    @Test
    void findByAuthorListsEachBookOnce() {
        CopiesLibrary copies = new CopiesLibrary();
        copies.addBook(dune);
        copies.addBook(new Book("Dune", "Frank Herbert", "111", 1965));
        copies.addBook(messiah);
        assertEquals(List.of(dune, messiah), copies.findByAuthor("frank herbert"));
    }

    // Uppgift 4

    @Test
    void allAuthorsIsDerivedFromTheBooks() {
        assertEquals(Set.of("Frank Herbert", "Isaac Asimov", "J.R.R. Tolkien"), library.allAuthors());
        library.removeBook("222");
        assertFalse(library.allAuthors().contains("J.R.R. Tolkien"));
    }

    @Test
    void allAuthorsCannotBeModifiedFromOutside() {
        assertThrows(UnsupportedOperationException.class, () -> library.allAuthors().add("Someone"));
    }

    @Test
    void genresCanExistWithoutAnyBooks() {
        library.registerGenre("Poetry");
        assertTrue(library.getGenres().contains("Poetry"));
    }

    // Uppgift 5

    @Test
    void naturalOrderIsNowByYear() {
        assertTrue(hobbit.compareTo(dune) < 0);
        assertEquals(List.of(hobbit, robots, foundation, dune, messiah), library.booksSortedByYear());
    }

    @Test
    void titleSortNeedsItsOwnComparator() {
        assertEquals(List.of(dune, messiah, foundation, robots, hobbit), library.booksSortedByTitle());
    }

    @Test
    void sameYearCompareAsEqualSoATreeSetDropsOne() {
        Book other1965 = new Book("The Three Stigmata of Palmer Eldritch", "Philip K. Dick", "666", 1965);
        TreeSet<Book> byYear = new TreeSet<>(List.of(dune, other1965));
        assertEquals(1, byYear.size());
    }
}
