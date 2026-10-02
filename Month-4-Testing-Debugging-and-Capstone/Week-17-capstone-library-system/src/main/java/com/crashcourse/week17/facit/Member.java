package com.crashcourse.week17.facit;

import java.util.ArrayList;
import java.util.List;

/** A library member: an id, a name, and the items they currently hold. */
public final class Member {

    private final String id;
    private final String name;
    private final int borrowingLimit;
    private final List<LibraryItem> borrowedItems = new ArrayList<>();

    public Member(String id, String name, int borrowingLimit) {
        if (id == null || id.isBlank()) {
            throw new IllegalArgumentException("Member id must not be blank");
        }
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Member name must not be blank");
        }
        if (borrowingLimit <= 0) {
            throw new IllegalArgumentException(
                "Borrowing limit must be positive, got " + borrowingLimit);
        }
        this.id = id;
        this.name = name;
        this.borrowingLimit = borrowingLimit;
    }

    public String id() {
        return id;
    }

    public String name() {
        return name;
    }

    public int borrowingLimit() {
        return borrowingLimit;
    }

    public List<LibraryItem> borrowedItems() {
        return List.copyOf(borrowedItems);
    }

    public boolean hasReachedBorrowingLimit() {
        return borrowedItems.size() >= borrowingLimit;
    }

    // Package-private: only Library orchestrates changes to a member's
    // borrowed-item list, so it can never drift out of sync with the
    // corresponding LibraryItem's own available/borrower state.
    void addBorrowedItem(LibraryItem item) {
        borrowedItems.add(item);
    }

    void removeBorrowedItem(LibraryItem item) {
        borrowedItems.remove(item);
    }
}
