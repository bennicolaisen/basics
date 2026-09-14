package com.crashcourse.week12;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * A small book catalog, and a working example of picking the right
 * collection for each job:
 *
 * <ul>
 *   <li>{@code Map<String, Book>} — books keyed by ISBN, for O(1) lookup,
 *       duplicate detection, and removal by the identifier that actually
 *       uniquely names a book.</li>
 *   <li>{@code List<Book>} — for every method that returns an ordered or
 *       filtered *sequence* of books ({@link #findByAuthor},
 *       {@link #booksSortedByYear}), since order and duplicates-allowed
 *       both matter there.</li>
 *   <li>{@code Set<String>} — {@link #genres}, since a genre either has
 *       been registered or hasn't; there's no meaningful order or count
 *       to a collection of genre names.</li>
 * </ul>
 */
public class Library {

    private final Map<String, Book> booksByIsbn = new HashMap<>();
    private final Set<String> genres = new HashSet<>();

    public void addBook(Book book) throws DuplicateIsbnException {
        if (book == null) {
            throw new IllegalArgumentException("book must not be null");
        }
        if (booksByIsbn.containsKey(book.getIsbn())) {
            throw new DuplicateIsbnException(book.getIsbn());
        }
        booksByIsbn.put(book.getIsbn(), book);
    }

    /** Removes the book with this ISBN, if present. Returns whether a book was removed. */
    public boolean removeBook(String isbn) {
        return booksByIsbn.remove(isbn) != null;
    }

    public Book findByIsbn(String isbn) {
        return booksByIsbn.get(isbn);
    }

    public int size() {
        return booksByIsbn.size();
    }

    public List<Book> findByAuthor(String author) {
        List<Book> matches = new ArrayList<>();
        for (Book book : booksByIsbn.values()) {
            if (book.getAuthor().equalsIgnoreCase(author)) {
                matches.add(book);
            }
        }
        return matches;
    }

    /**
     * Books ordered by publication year, ascending. Uses a
     * {@link Comparator} rather than {@link Book}'s natural
     * (title-based) ordering from {@link Comparable}, to show the two
     * side by side: this method wants a *different* ordering than the
     * class's own "natural" one, without changing {@code Book} itself.
     */
    public List<Book> booksSortedByYear() {
        List<Book> books = new ArrayList<>(booksByIsbn.values());
        books.sort(Comparator.comparingInt(Book::getYear));
        return books;
    }

    /** All books currently in the library, in no particular order. */
    public Collection<Book> allBooks() {
        return Collections.unmodifiableCollection(booksByIsbn.values());
    }

    /** Registers a genre name as one this library catalogs books under. */
    public void registerGenre(String genre) {
        if (genre == null || genre.isBlank()) {
            throw new IllegalArgumentException("genre must not be blank");
        }
        genres.add(genre);
    }

    /** Every genre registered so far, as an unmodifiable set. */
    public Set<String> getGenres() {
        return Collections.unmodifiableSet(genres);
    }
}
