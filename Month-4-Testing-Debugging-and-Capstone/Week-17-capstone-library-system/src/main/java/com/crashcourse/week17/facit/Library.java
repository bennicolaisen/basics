package com.crashcourse.week17.facit;

import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.OptionalInt;

/**
 * Facit: Library med förlängning (uppgift 2), reservationer (uppgift 3),
 * förfallna lån per medlem (uppgift 4) och gränser per sort (uppgift 5).
 * Se FACIT.md.
 */
public final class Library {

    private final Map<String, LibraryItem> catalog = new HashMap<>();
    private final Map<String, Member> members = new HashMap<>();
    private final Map<String, HoldQueue> holds = new HashMap<>();
    private final BorrowingPolicy policy;

    public Library() {
        this(new BorrowingPolicy());
    }

    /** Uppgift 5: gränserna per sort är bibliotekets regler och ges till biblioteket. */
    public Library(BorrowingPolicy policy) {
        if (policy == null) {
            throw new IllegalArgumentException("Policy must not be null");
        }
        this.policy = policy;
    }

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
        HoldQueue queue = holds.get(itemId);
        if (queue != null && queue.isReservedForSomeoneOtherThan(member)) {
            throw new ItemNotAvailableException(
                "Item " + itemId + " (" + item.title() + ") is reserved for another member");
        }
        if (member.hasReachedBorrowingLimit()) {
            throw new BorrowingLimitExceededException(
                "Member " + memberId + " has reached their borrowing limit of "
                    + member.borrowingLimit());
        }
        OptionalInt typeLimit = policy.limitFor(item.getClass());
        if (typeLimit.isPresent() && countOfType(member, item.getClass()) >= typeLimit.getAsInt()) {
            throw new BorrowingLimitExceededException(
                "Member " + memberId + " may borrow at most " + typeLimit.getAsInt()
                    + " " + item.getClass().getSimpleName() + " at a time");
        }

        item.checkOut(member);
        member.addBorrowedItem(item);
        if (queue != null) {
            queue.pickedUpBy(member);
        }
        return item;
    }

    /**
     * Lämnar tillbaka ett exemplar. Står någon i kön reserveras det för den
     * som står först, i stället för att gå tillbaka till alla (uppgift 3).
     */
    public void returnItem(String memberId, String itemId) throws MemberNotFoundException {
        Member member = requireMember(memberId);
        LibraryItem item = requireBorrowedBy(member, itemId);

        item.returnItem();
        member.removeBorrowedItem(item);
        HoldQueue queue = holds.get(itemId);
        if (queue != null) {
            queue.itemReturned();
        }
    }

    /**
     * Uppgift 2: förlänger lånet med en låneperiod till. Går inte om någon
     * annan står i kö för exemplaret.
     */
    public LocalDate renew(String memberId, String itemId)
            throws MemberNotFoundException, ItemNotAvailableException {
        Member member = requireMember(memberId);
        LibraryItem item = requireBorrowedBy(member, itemId);

        HoldQueue queue = holds.get(itemId);
        if (queue != null && queue.hasWaiting()) {
            throw new ItemNotAvailableException(
                "Item " + itemId + " (" + item.title() + ") cannot be renewed: other members are waiting for it");
        }
        item.extendDueDate();
        return item.dueDate();
    }

    /** Uppgift 3: ställer medlemmen i kö för ett exemplar som inte går att låna just nu. */
    public void placeHold(String memberId, String itemId) throws MemberNotFoundException {
        Member member = requireMember(memberId);
        LibraryItem item = requireItem(itemId);
        if (item.currentBorrower() == member) {
            throw new IllegalStateException("Member " + memberId + " is already borrowing item " + itemId);
        }
        HoldQueue queue = holds.computeIfAbsent(itemId, id -> new HoldQueue());
        if (item.isAvailable() && !queue.isReservedForSomeoneOtherThan(member)) {
            throw new IllegalStateException("Item " + itemId + " is available; check it out instead");
        }
        queue.place(member);
    }

    /** Kön för ett exemplar; tom om ingen har reserverat det. */
    public HoldQueue holdsFor(String itemId) {
        requireItem(itemId);
        return holds.getOrDefault(itemId, new HoldQueue());
    }

    public List<LibraryItem> overdueItems(LocalDate today) {
        return catalog.values().stream()
            .filter(item -> isOverdue(item, today))
            .toList();
    }

    /** Uppgift 4: bara den här medlemmens förfallna lån. */
    public List<LibraryItem> overdueItemsForMember(String memberId, LocalDate today) {
        Member member = requireMember(memberId);
        return member.borrowedItems().stream()
            .filter(item -> isOverdue(item, today))
            .toList();
    }

    private static boolean isOverdue(LibraryItem item, LocalDate today) {
        return !item.isAvailable() && item.dueDate() != null && today.isAfter(item.dueDate());
    }

    private static long countOfType(Member member, Class<?> type) {
        return member.borrowedItems().stream()
            .filter(borrowed -> borrowed.getClass() == type)
            .count();
    }

    private Member requireMember(String memberId) {
        Member member = members.get(memberId);
        if (member == null) {
            throw new MemberNotFoundException("No member with id " + memberId);
        }
        return member;
    }

    private LibraryItem requireItem(String itemId) {
        LibraryItem item = catalog.get(itemId);
        if (item == null) {
            throw new IllegalArgumentException("No item with id " + itemId + " in the catalog");
        }
        return item;
    }

    /**
     * Exemplaret måste finnas och vara utlånat till just den här medlemmen.
     * Originalets returnItem kontrollerade bara att exemplaret var utlånat,
     * inte till vem; se FACIT.md.
     */
    private LibraryItem requireBorrowedBy(Member member, String itemId) {
        LibraryItem item = requireItem(itemId);
        if (item.isAvailable()) {
            throw new IllegalStateException("Item " + itemId + " is not currently checked out");
        }
        if (item.currentBorrower() != member) {
            throw new IllegalStateException(
                "Item " + itemId + " is not checked out by member " + member.id());
        }
        return item;
    }
}
