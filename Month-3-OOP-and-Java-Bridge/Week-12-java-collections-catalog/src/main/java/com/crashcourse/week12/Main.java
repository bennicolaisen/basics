package com.crashcourse.week12;

import java.util.Collections;
import java.util.List;

public class Main {

    public static void main(String[] args) throws DuplicateIsbnException {
        Library library = new Library();
        library.registerGenre("Science Fiction");
        library.registerGenre("Fantasy");

        library.addBook(new Book("Dune", "Frank Herbert", "978-0441013593", 1965));
        library.addBook(new Book("The Hobbit", "J.R.R. Tolkien", "978-0547928227", 1937));
        library.addBook(new Book("Foundation", "Isaac Asimov", "978-0553293357", 1951));

        System.out.println("Books sorted by year:");
        for (Book book : library.booksSortedByYear()) {
            System.out.println("  " + book);
        }

        List<Book> naturalOrder = library.booksSortedByYear();
        Collections.sort(naturalOrder); // Book's natural (title) ordering via Comparable
        System.out.println("Same books, natural (title) order:");
        for (Book book : naturalOrder) {
            System.out.println("  " + book);
        }

        System.out.println("Registered genres: " + library.getGenres());
    }
}
