package com.crashcourse.week12;

import java.util.Objects;

/**
 * A book with a title, author, ISBN, and publication year.
 *
 * <p>Implements {@link Comparable}&lt;Book&gt; to give books one natural
 * ordering (by title) — see {@link Library#booksSortedByYear()} for the
 * alternative, a {@code Comparator}, used when a *different* ordering is
 * needed without changing what "natural" means for a `Book`.
 *
 * <p>{@code equals}/{@code hashCode} are based on ISBN alone: two `Book`
 * objects with the same ISBN are considered the same book, regardless of
 * what their other fields say (an ISBN, in reality, uniquely identifies
 * an edition of a book).
 */
public class Book implements Comparable<Book> {

    private final String title;
    private final String author;
    private final String isbn;
    private final int year;

    public Book(String title, String author, String isbn, int year) {
        if (title == null || title.isBlank()) {
            throw new IllegalArgumentException("title must not be blank");
        }
        if (author == null || author.isBlank()) {
            throw new IllegalArgumentException("author must not be blank");
        }
        if (isbn == null || isbn.isBlank()) {
            throw new IllegalArgumentException("isbn must not be blank");
        }
        if (year <= 0) {
            throw new IllegalArgumentException("year must be > 0, got " + year);
        }
        this.title = title;
        this.author = author;
        this.isbn = isbn;
        this.year = year;
    }

    public String getTitle() {
        return title;
    }

    public String getAuthor() {
        return author;
    }

    public String getIsbn() {
        return isbn;
    }

    public int getYear() {
        return year;
    }

    /** Natural ordering: by title, case-insensitively. */
    @Override
    public int compareTo(Book other) {
        return this.title.compareToIgnoreCase(other.title);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (!(obj instanceof Book other)) {
            return false;
        }
        return isbn.equals(other.isbn);
    }

    @Override
    public int hashCode() {
        return Objects.hash(isbn);
    }

    @Override
    public String toString() {
        return String.format("%s by %s (%d) [ISBN %s]", title, author, year, isbn);
    }
}
