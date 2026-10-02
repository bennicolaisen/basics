package com.crashcourse.week12.facit;

import java.util.Objects;

/**
 * Facit, uppgift 5: Book med naturlig ordning efter utgivningsår i stället
 * för titel. Allt annat är oförändrat jämfört med com.crashcourse.week12.Book.
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

    /** Uppgift 5: naturlig ordning efter år, äldst först. */
    @Override
    public int compareTo(Book other) {
        return Integer.compare(this.year, other.year);
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
