package com.crashcourse.week15;

/**
 * A pricing strategy that transforms a running total for a purchase of some
 * quantity of an {@link Item}. Multiple discounts are applied in sequence
 * by {@link PriceCalculator}, each receiving the total left over from the
 * one before it.
 */
public interface Discount {

    /**
     * Returns the new running total after this discount is applied.
     *
     * @param runningTotal the total so far, after any earlier discounts
     * @param item the item being purchased (its original base price is
     *             available even after earlier discounts have changed the
     *             running total)
     * @param quantity how many units are being purchased
     */
    double applyTo(double runningTotal, Item item, int quantity);

    /** A short, human-readable description, e.g. for a receipt line. */
    String description();
}
