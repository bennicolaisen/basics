package com.crashcourse.week17;

import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * The orchestrator: owns the catalog and the membership, and is the only
 * class that coordinates a checkout or return across a {@link Member} and
 * a {@link LibraryItem} - neither of those two classes talks to the other
 * directly.
 */
public final class Library {

    private final Map<String, LibraryItem> catalog = new HashMap<>();
    private final Map<String, Member> members = new HashMap<>();

    public void addItem(LibraryItem item) {
        if (item == null) {
            throw new IllegalArgumentException("Item must not be null");
        }
        catalog.put(item.id(), item);
    }

    public void addMember(Member member) {
        if (member == null) {
            throw new IllegalArgumentException("Member must not be null");
        }
        members.put(member.id(), member);
    }

    public LibraryItem findItem(String itemId) {
        return catalog.get(itemId);
    }

    public Member findMember(String memberId) {
        return members.get(memberId);
    }

    /**
     * Checks item {@code itemId} out to member {@code memberId}, validating
     * (in order) that the member exists, the item exists and is available,
     * and the member has not reached their borrowing limit - throwing the
     * exception that matches whichever condition fails first.
     */
    public LibraryItem checkOut(String memberId, String itemId)
            throws MemberNotFoundException, ItemNotAvailableException, BorrowingLimitExceededException {
        Member member = requireMember(memberId);

        LibraryItem item = catalog.get(itemId);
        if (item == null) {
            throw new ItemNotAvailableException("No item with id " + itemId + " in the catalog");
        }
        if (!item.isAvailable()) {
            throw new ItemNotAvailableException(
                "Item " + itemId + " (" + item.title() + ") is currently checked out");
        }
        if (member.hasReachedBorrowingLimit()) {
            throw new BorrowingLimitExceededException(
                "Member " + memberId + " has reached their borrowing limit of "
                    + member.borrowingLimit());
        }

        item.checkOut(member);
        member.addBorrowedItem(item);
        return item;
    }

    /** Returns item {@code itemId} on behalf of member {@code memberId}. */
    public void returnItem(String memberId, String itemId) throws MemberNotFoundException {
        Member member = requireMember(memberId);

        LibraryItem item = catalog.get(itemId);
        if (item == null) {
            throw new IllegalArgumentException("No item with id " + itemId + " in the catalog");
        }
        if (item.isAvailable()) {
            throw new IllegalStateException("Item " + itemId + " is not currently checked out");
        }

        item.returnItem();
        member.removeBorrowedItem(item);
    }

    /** Every checked-out item whose due date is before {@code today}. */
    public List<LibraryItem> overdueItems(LocalDate today) {
        return catalog.values().stream()
            .filter(item -> !item.isAvailable() && item.dueDate() != null && today.isAfter(item.dueDate()))
            .toList();
    }

    private Member requireMember(String memberId) {
        Member member = members.get(memberId);
        if (member == null) {
            throw new MemberNotFoundException("No member with id " + memberId);
        }
        return member;
    }
}
