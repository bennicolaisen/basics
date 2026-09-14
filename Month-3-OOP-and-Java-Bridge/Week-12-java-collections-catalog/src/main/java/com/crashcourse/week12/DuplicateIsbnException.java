package com.crashcourse.week12;

/** Raised when a book is added whose ISBN already exists in the Library. */
public class DuplicateIsbnException extends Exception {

    public DuplicateIsbnException(String isbn) {
        super("a book with ISBN " + isbn + " already exists in this library");
    }
}
