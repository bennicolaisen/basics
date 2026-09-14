package com.crashcourse.week17;

/** A library book: title, author, and ISBN, with a three-week loan period. */
public final class Book extends LibraryItem {

    private static final int LOAN_PERIOD_DAYS = 21;

    private final String author;
    private final String isbn;

    public Book(String id, String title, String author, String isbn) {
        super(id, title);
        if (author == null || author.isBlank()) {
            throw new IllegalArgumentException("Author must not be blank");
        }
        if (isbn == null || isbn.isBlank()) {
            throw new IllegalArgumentException("ISBN must not be blank");
        }
        this.author = author;
        this.isbn = isbn;
    }

    public String author() {
        return author;
    }

    public String isbn() {
        return isbn;
    }

    @Override
    public int loanPeriodDays() {
        return LOAN_PERIOD_DAYS;
    }
}
