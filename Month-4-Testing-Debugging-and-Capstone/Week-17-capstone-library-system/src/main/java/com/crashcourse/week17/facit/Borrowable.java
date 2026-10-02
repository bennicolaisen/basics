package com.crashcourse.week17.facit;

/**
 * Anything that can be checked out to a {@link Member} and later returned.
 * Implemented by {@link LibraryItem}, so every concrete item type (
 * {@link Book}, {@link DVD}, {@link Magazine}) is borrowable by inheriting
 * one shared implementation rather than each reimplementing it.
 */
public interface Borrowable {

    /**
     * Checks this item out to {@code member}.
     *
     * @throws ItemNotAvailableException if this item is already checked out
     */
    void checkOut(Member member) throws ItemNotAvailableException;

    /** Marks this item as returned and available again. */
    void returnItem();

    boolean isAvailable();
}
