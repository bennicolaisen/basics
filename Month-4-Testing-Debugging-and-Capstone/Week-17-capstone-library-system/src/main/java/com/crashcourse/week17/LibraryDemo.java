package com.crashcourse.week17;

import java.time.LocalDate;

/** A small runnable walkthrough of the Library system's happy path. */
public final class LibraryDemo {

    public static void main(String[] args) throws Exception {
        Library library = new Library();

        library.addItem(new Book("B1", "Effective Java", "Joshua Bloch", "978-0134685991"));
        library.addItem(new DVD("D1", "The Matrix", 136));
        library.addItem(new Magazine("M1", "National Geographic", 250));

        Member alice = new Member("MEM1", "Alice", 2);
        library.addMember(alice);

        library.checkOut("MEM1", "B1");
        System.out.println("Alice checked out: " + library.findItem("B1"));

        library.checkOut("MEM1", "D1");
        System.out.println("Alice checked out: " + library.findItem("D1"));

        try {
            library.checkOut("MEM1", "M1");
        } catch (BorrowingLimitExceededException e) {
            System.out.println("Expected failure: " + e.getMessage());
        }

        System.out.println("Overdue right now: " + library.overdueItems(LocalDate.now()));

        library.returnItem("MEM1", "B1");
        System.out.println("Alice returned Effective Java. Now borrowing: " + alice.borrowedItems());
    }
}
