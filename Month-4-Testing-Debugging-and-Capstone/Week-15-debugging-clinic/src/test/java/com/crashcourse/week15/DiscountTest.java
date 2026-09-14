package com.crashcourse.week15;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class DiscountTest {

    private static final double DELTA = 1e-9;
    private final Item item = new Item("SKU-1", "Widget", 100.0);

    @Test
    @DisplayName("PercentageDiscount reduces the running total by the given percentage")
    void percentageDiscountReducesTotal() {
        Discount discount = new PercentageDiscount(25);

        assertEquals(75.0, discount.applyTo(100.0, item, 1), DELTA);
    }

    @Test
    @DisplayName("PercentageDiscount rejects a value outside 0-100")
    void percentageDiscountRejectsOutOfRange() {
        assertThrows(IllegalArgumentException.class, () -> new PercentageDiscount(150));
        assertThrows(IllegalArgumentException.class, () -> new PercentageDiscount(-10));
    }

    @Test
    @DisplayName("FlatAmountDiscount subtracts a fixed amount from the running total")
    void flatAmountDiscountSubtractsAmount() {
        Discount discount = new FlatAmountDiscount(15.0);

        assertEquals(85.0, discount.applyTo(100.0, item, 1), DELTA);
    }

    @Test
    @DisplayName("FlatAmountDiscount never takes the running total below zero")
    void flatAmountDiscountFloorsAtZero() {
        Discount discount = new FlatAmountDiscount(500.0);

        assertEquals(0.0, discount.applyTo(100.0, item, 1), DELTA);
    }

    @Test
    @DisplayName("FlatAmountDiscount rejects a negative amount")
    void flatAmountDiscountRejectsNegative() {
        assertThrows(IllegalArgumentException.class, () -> new FlatAmountDiscount(-5.0));
    }

    @Test
    @DisplayName("BuyOneGetOneDiscount gives back the price of one free unit per pair purchased")
    void buyOneGetOneDiscountsPairs() {
        Discount discount = new BuyOneGetOneDiscount();
        // 4 units at $100 base each = $400 running total; 2 pairs -> 2 free units -> $200 off
        assertEquals(200.0, discount.applyTo(400.0, item, 4), DELTA);
    }

    @Test
    @DisplayName("BuyOneGetOneDiscount gives no discount for an odd unit left unpaired")
    void buyOneGetOneDiscountLeavesOddUnitFullPrice() {
        Discount discount = new BuyOneGetOneDiscount();
        // 3 units: only 1 full pair -> 1 free unit -> $100 off
        assertEquals(200.0, discount.applyTo(300.0, item, 3), DELTA);
    }

    @Test
    @DisplayName("BuyOneGetOneDiscount gives no discount for a single unit")
    void buyOneGetOneDiscountNoPairs() {
        Discount discount = new BuyOneGetOneDiscount();

        assertEquals(100.0, discount.applyTo(100.0, item, 1), DELTA);
    }
}
