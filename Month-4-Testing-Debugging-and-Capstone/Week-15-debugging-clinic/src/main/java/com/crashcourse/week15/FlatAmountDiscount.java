package com.crashcourse.week15;

/** Reduces the running total by a fixed amount, never going below zero. */
public final class FlatAmountDiscount implements Discount {

    private final double amountOff;

    public FlatAmountDiscount(double amountOff) {
        if (amountOff < 0) {
            throw new IllegalArgumentException("Amount off must not be negative, got " + amountOff);
        }
        this.amountOff = amountOff;
    }

    @Override
    public double applyTo(double runningTotal, Item item, int quantity) {
        return Math.max(0, runningTotal - amountOff);
    }

    @Override
    public String description() {
        return "$%.2f off".formatted(amountOff);
    }
}
