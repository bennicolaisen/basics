package com.crashcourse.week12.facit;

/** Facit: oförändrad jämfört med com.crashcourse.week12.DuplicateIsbnException. */
public class DuplicateIsbnException extends Exception {

    public DuplicateIsbnException(String isbn) {
        super("a book with ISBN " + isbn + " already exists in this library");
    }
}
