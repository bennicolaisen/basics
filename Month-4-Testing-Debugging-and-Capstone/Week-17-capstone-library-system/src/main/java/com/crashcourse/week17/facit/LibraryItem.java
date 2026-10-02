package com.crashcourse.week17.facit;

import java.time.LocalDate;

/**
 * Common state and behavior for anything the library catalogs: an id, a
 * title, and the shared mechanics of being checked out and returned.
 * {@link Book}, {@link DVD}, and {@link Magazine} each add their own
 * type-specific fields and their own loan period, but none of them need to
 * reimplement checkout bookkeeping - that lives here, once.
 */
public abstract class LibraryItem implements Borrowable {

    private final String id;
    private final String title;
    private boolean available = true;
    private Member currentBorrower;
    private LocalDate dueDate;

    protected LibraryItem(String id, String title) {
        if (id == null || id.isBlank()) {
            throw new IllegalArgumentException("Item id must not be blank");
        }
        if (title == null || title.isBlank()) {
            throw new IllegalArgumentException("Item title must not be blank");
        }
        this.id = id;
        this.title = title;
    }

    public String id() {
        return id;
    }

    public String title() {
        return title;
    }

    @Override
    public boolean isAvailable() {
        return available;
    }

    public Member currentBorrower() {
        return currentBorrower;
    }

    public LocalDate dueDate() {
        return dueDate;
    }

    /** Type-specific loan length in days, used to derive a due date at checkout. */
    public abstract int loanPeriodDays();

    @Override
    public void checkOut(Member member) throws ItemNotAvailableException {
        if (!available) {
            throw new ItemNotAvailableException(
                "Item " + id + " (" + title + ") is currently checked out");
        }
        this.available = false;
        this.currentBorrower = member;
        this.dueDate = LocalDate.now().plusDays(loanPeriodDays());
    }

    /**
     * Facit, uppgift 2: förlänger lånet med en hel låneperiod till, räknat
     * från det nuvarande förfallodatumet. Paketprivat: bara Library får
     * förlänga, efter att ha kontrollerat vem som lånar.
     */
    void extendDueDate() {
        if (available) {
            throw new IllegalStateException("Item " + id + " is not checked out");
        }
        this.dueDate = dueDate.plusDays(loanPeriodDays());
    }

    @Override
    public void returnItem() {
        this.available = true;
        this.currentBorrower = null;
        this.dueDate = null;
    }

    @Override
    public String toString() {
        return "%s{id='%s', title='%s', available=%s}"
            .formatted(getClass().getSimpleName(), id, title, available);
    }
}
