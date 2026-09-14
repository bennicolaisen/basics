package com.crashcourse.week15;

/** Reduces the running total by a fixed percentage. */
public final class PercentageDiscount implements Discount {

    private final double percentOff;

    public PercentageDiscount(double percentOff) {
        if (percentOff < 0 || percentOff > 100) {
            throw new IllegalArgumentException(
                "Percent off must be between 0 and 100, got " + percentOff);
        }
        this.percentOff = percentOff;
    }

    @Override
    public double applyTo(double runningTotal, Item item, int quantity) {
        return runningTotal * (1 - percentOff / 100.0);
    }

    @Override
    public String description() {
        return "%.0f%% off".formatted(percentOff);
    }
}
