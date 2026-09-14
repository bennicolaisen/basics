package com.crashcourse.week12;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Collections;
import java.util.List;
import org.junit.jupiter.api.Test;

class LibraryTest {

    private Book dune() {
        return new Book("Dune", "Frank Herbert", "111", 1965);
    }

    private Book hobbit() {
        return new Book("The Hobbit", "J.R.R. Tolkien", "222", 1937);
    }

    private Book foundation() {
        return new Book("Foundation", "Isaac Asimov", "333", 1951);
    }

    @Test
    void addAndFindByIsbn() throws DuplicateIsbnException {
        Library library = new Library();
        library.addBook(dune());
        assertEquals("Dune", library.findByIsbn("111").getTitle());
        assertEquals(1, library.size());
    }

    @Test
    void addingDuplicateIsbnThrows() throws DuplicateIsbnException {
        Library library = new Library();
        library.addBook(dune());
        Book sameIsbnDifferentBook = new Book("Dune Messiah", "Frank Herbert", "111", 1969);
        assertThrows(DuplicateIsbnException.class, () -> library.addBook(sameIsbnDifferentBook));
        // The original registration is untouched.
        assertEquals("Dune", library.findByIsbn("111").getTitle());
        assertEquals(1, library.size());
    }

    @Test
    void removeBookRemovesByIsbn() throws DuplicateIsbnException {
        Library library = new Library();
        library.addBook(dune());
        assertTrue(library.removeBook("111"));
        assertNull(library.findByIsbn("111"));
        assertEquals(0, library.size());
    }

    @Test
    void removingUnknownIsbnReturnsFalse() {
        Library library = new Library();
        assertFalse(library.removeBook("does-not-exist"));
    }

    @Test
    void findByAuthorIsCaseInsensitiveAndReturnsAllMatches() throws DuplicateIsbnException {
        Library library = new Library();
        library.addBook(dune());
        library.addBook(new Book("Dune Messiah", "Frank Herbert", "999", 1969));
        library.addBook(hobbit());

        List<Book> byHerbert = library.findByAuthor("frank herbert");
        assertEquals(2, byHerbert.size());

        List<Book> byUnknown = library.findByAuthor("Nobody");
        assertTrue(byUnknown.isEmpty());
    }

    @Test
    void booksSortedByYearUsesComparatorNotNaturalOrder() throws DuplicateIsbnException {
        Library library = new Library();
        library.addBook(dune()); // 1965
        library.addBook(hobbit()); // 1937
        library.addBook(foundation()); // 1951

        List<Book> byYear = library.booksSortedByYear();
        assertEquals(List.of("The Hobbit", "Foundation", "Dune"),
                byYear.stream().map(Book::getTitle).toList());

        // Natural order (by title, via Comparable) is a different ordering
        // from booksSortedByYear's Comparator-based one: sorting the same
        // three books with Collections.sort (which uses Book.compareTo)
        // gives title order, not year order.
        List<Book> byTitle = new java.util.ArrayList<>(byYear);
        Collections.sort(byTitle);
        assertEquals(List.of("Dune", "Foundation", "The Hobbit"),
                byTitle.stream().map(Book::getTitle).toList());
    }

    @Test
    void genresAreTrackedAsASet() {
        Library library = new Library();
        library.registerGenre("Science Fiction");
        library.registerGenre("Fantasy");
        library.registerGenre("Science Fiction"); // duplicate registration, ignored

        assertEquals(2, library.getGenres().size());
        assertTrue(library.getGenres().contains("Fantasy"));
    }

    @Test
    void addingNullBookRejected() {
        Library library = new Library();
        assertThrows(IllegalArgumentException.class, () -> library.addBook(null));
    }
}
