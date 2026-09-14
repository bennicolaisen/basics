package com.crashcourse.week15;

/**
 * "Buy one, get one free": for every two units purchased, one is free.
 *
 * <p>The free units' value is computed from the item's original
 * {@link Item#basePrice()}, not from {@code runningTotal} - "buy one get
 * one" is a statement about physical units ("every second one is free"),
 * so it must be priced off the item's real unit price regardless of what
 * percentage or flat discounts were applied to the running total before
 * this one in the sequence.
 */
public final class BuyOneGetOneDiscount implements Discount {

    @Override
    public double applyTo(double runningTotal, Item item, int quantity) {
        int freeUnits = quantity / 2;
        double discountAmount = freeUnits * item.basePrice();
        return Math.max(0, runningTotal - discountAmount);
    }

    @Override
    public String description() {
        return "Buy one, get one free";
    }
}
