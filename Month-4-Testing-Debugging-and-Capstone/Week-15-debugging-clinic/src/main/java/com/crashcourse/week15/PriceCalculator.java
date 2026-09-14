package com.crashcourse.week15;

import java.util.List;

/** Ties {@link Item} and {@link Discount} together to price a purchase. */
public final class PriceCalculator {

    public double calculateFinalPrice(Item item, int quantity, List<Discount> discounts) {
        if (item == null) {
            throw new IllegalArgumentException("Item must not be null");
        }
        if (quantity <= 0) {
            throw new IllegalArgumentException("Quantity must be positive, got " + quantity);
        }
        if (discounts == null) {
            throw new IllegalArgumentException("Discounts list must not be null");
        }

        double total = item.basePrice() * quantity;
        for (Discount discount : discounts) {
            total = discount.applyTo(total, item, quantity);
        }
        return total;
    }

    /**
     * The final price divided evenly across every unit purchased. Safe by
     * construction: {@link #calculateFinalPrice} above always validates
     * {@code quantity > 0} before this division ever runs.
     */
    public double averagePricePerUnit(Item item, int quantity, List<Discount> discounts) {
        double finalPrice = calculateFinalPrice(item, quantity, discounts);
        return finalPrice / quantity;
    }
}
