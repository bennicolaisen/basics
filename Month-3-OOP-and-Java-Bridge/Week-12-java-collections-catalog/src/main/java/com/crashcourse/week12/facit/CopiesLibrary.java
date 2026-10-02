package com.crashcourse.week12.facit;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Facit, uppgift 3: ett bibliotek som kan äga flera exemplar av samma bok.
 *
 * <p>Varje ISBN pekar nu på en lista med exemplar. Tre saker ändras:
 * <ul>
 *   <li>addBook: ett ISBN som redan finns är inte längre ett fel, utan ett
 *       nytt exemplar. Dubblettkontrollen blir i stället en
 *       konsistenskontroll: ett nytt exemplar måste ha samma titel,
 *       författare och år som de exemplar som redan finns.</li>
 *   <li>removeBook: tar bort <em>ett</em> exemplar. När det sista
 *       exemplaret tas bort måste nyckeln tas bort ur mappen, annars ligger
 *       en tom lista kvar och ISBN:et ser ut att finnas.</li>
 *   <li>size: det finns nu två storlekar, antal exemplar och antal olika
 *       titlar.</li>
 * </ul>
 */
public class CopiesLibrary {

    private final Map<String, List<Book>> booksByIsbn = new HashMap<>();

    /** Lägger till ett exemplar. Kastar om ISBN:et redan används för en annan bok. */
    public void addBook(Book book) {
        if (book == null) {
            throw new IllegalArgumentException("book must not be null");
        }
        List<Book> copies = booksByIsbn.get(book.getIsbn());
        if (copies == null) {
            copies = new ArrayList<>();
            booksByIsbn.put(book.getIsbn(), copies);
        } else if (!sameEdition(copies.get(0), book)) {
            throw new IllegalArgumentException(
                    "ISBN " + book.getIsbn() + " already belongs to " + copies.get(0));
        }
        copies.add(book);
    }

    /** Tar bort ett exemplar. Returnerar om något exemplar fanns att ta bort. */
    public boolean removeBook(String isbn) {
        List<Book> copies = booksByIsbn.get(isbn);
        if (copies == null) {
            return false;
        }
        copies.remove(copies.size() - 1);
        if (copies.isEmpty()) {
            booksByIsbn.remove(isbn);
        }
        return true;
    }

    /** Ett exemplar av boken, eller null om biblioteket inte har den. */
    public Book findByIsbn(String isbn) {
        List<Book> copies = booksByIsbn.get(isbn);
        return copies == null ? null : copies.get(0);
    }

    public int copiesOf(String isbn) {
        List<Book> copies = booksByIsbn.get(isbn);
        return copies == null ? 0 : copies.size();
    }

    /** Antal exemplar totalt. */
    public int size() {
        int total = 0;
        for (List<Book> copies : booksByIsbn.values()) {
            total += copies.size();
        }
        return total;
    }

    /** Antal olika böcker (olika ISBN), oavsett hur många exemplar. */
    public int titleCount() {
        return booksByIsbn.size();
    }

    /** Varje bok av författaren en gång, även om biblioteket har flera exemplar. */
    public List<Book> findByAuthor(String author) {
        List<Book> matches = new ArrayList<>();
        for (List<Book> copies : booksByIsbn.values()) {
            Book book = copies.get(0);
            if (book.getAuthor().equalsIgnoreCase(author)) {
                matches.add(book);
            }
        }
        Collections.sort(matches);
        return matches;
    }

    private static boolean sameEdition(Book a, Book b) {
        return a.getTitle().equals(b.getTitle())
                && a.getAuthor().equals(b.getAuthor())
                && a.getYear() == b.getYear();
    }
}
