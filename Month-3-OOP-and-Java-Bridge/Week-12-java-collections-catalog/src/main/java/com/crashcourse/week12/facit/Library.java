package com.crashcourse.week12.facit;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

/**
 * Facit: Library efter uppgift 1, 2, 4 och 5. Uppgift 3 (flera exemplar
 * per ISBN) ändrar hur hela klassen lagrar böcker och finns därför i en
 * egen klass, {@link CopiesLibrary}. Se FACIT.md.
 */
public class Library {

    private static final Comparator<Book> BY_AUTHOR_THEN_TITLE =
            Comparator.comparing(Book::getAuthor, String.CASE_INSENSITIVE_ORDER)
                    .thenComparing(Book::getTitle, String.CASE_INSENSITIVE_ORDER);

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
     * Uppgift 1: böcker utgivna från och med {@code from} till och med
     * {@code to}, sorterade efter år. Båda gränserna ingår, precis som när
     * man säger "böcker från 1950 till 1960".
     */
    public List<Book> findByYearRange(int from, int to) {
        if (from > to) {
            throw new IllegalArgumentException("from (" + from + ") must not be after to (" + to + ")");
        }
        List<Book> matches = new ArrayList<>();
        for (Book book : booksByIsbn.values()) {
            if (book.getYear() >= from && book.getYear() <= to) {
                matches.add(book);
            }
        }
        Collections.sort(matches);
        return matches;
    }

    /** Uppgift 2: sortera efter författare, och efter titel när författaren är samma. */
    public List<Book> booksSortedByAuthorThenTitle() {
        List<Book> books = new ArrayList<>(booksByIsbn.values());
        books.sort(BY_AUTHOR_THEN_TITLE);
        return books;
    }

    /** Uppgift 5: Book är nu Comparable efter år, så ingen Comparator behövs. */
    public List<Book> booksSortedByYear() {
        List<Book> books = new ArrayList<>(booksByIsbn.values());
        Collections.sort(books);
        return books;
    }

    /**
     * Efter uppgift 5 är titel inte längre den naturliga ordningen, så en
     * titelsortering måste uttryckligen ange sin Comparator.
     */
    public List<Book> booksSortedByTitle() {
        List<Book> books = new ArrayList<>(booksByIsbn.values());
        books.sort(Comparator.comparing(Book::getTitle, String.CASE_INSENSITIVE_ORDER));
        return books;
    }

    /**
     * Uppgift 4: författarna räknas fram ur böckerna varje gång, i stället för
     * att sparas i ett eget fält. En TreeSet ger dem i bokstavsordning.
     */
    public Set<String> allAuthors() {
        Set<String> authors = new TreeSet<>();
        for (Book book : booksByIsbn.values()) {
            authors.add(book.getAuthor());
        }
        return Collections.unmodifiableSet(authors);
    }

    public Collection<Book> allBooks() {
        return Collections.unmodifiableCollection(booksByIsbn.values());
    }

    public void registerGenre(String genre) {
        if (genre == null || genre.isBlank()) {
            throw new IllegalArgumentException("genre must not be blank");
        }
        genres.add(genre);
    }

    public Set<String> getGenres() {
        return Collections.unmodifiableSet(genres);
    }
}
