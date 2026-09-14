package com.crashcourse.week15;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class PriceCalculatorTest {

    private static final double DELTA = 1e-9;

    private PriceCalculator calculator;
    private Item item;

    @BeforeEach
    void setUp() {
        calculator = new PriceCalculator();
        item = new Item("SKU-1", "Widget", 50.0);
    }

    @Test
    @DisplayName("with no discounts, the final price is base price times quantity")
    void noDiscountsMultipliesQuantity() {
        double result = calculator.calculateFinalPrice(item, 3, List.of());

        assertEquals(150.0, result, DELTA);
    }

    @Test
    @DisplayName("multiple discounts are applied in sequence, each on the previous result")
    void discountsApplyInSequence() {
        // 2 units at $50 = $100 running total
        // PercentageDiscount(10%): 100 -> 90
        // FlatAmountDiscount($5): 90 -> 85
        List<Discount> discounts = List.of(new PercentageDiscount(10), new FlatAmountDiscount(5));

        double result = calculator.calculateFinalPrice(item, 2, discounts);

        assertEquals(85.0, result, DELTA);
    }

    @Test
    @DisplayName("a BuyOneGetOneDiscount combined with a percentage discount prices both correctly")
    void combinesBogoAndPercentage() {
        // 4 units at $50 = $200 running total
        // BOGO: 2 free units * $50 = $100 off -> 100
        // PercentageDiscount(10%): 100 -> 90
        List<Discount> discounts = List.of(new BuyOneGetOneDiscount(), new PercentageDiscount(10));

        double result = calculator.calculateFinalPrice(item, 4, discounts);

        assertEquals(90.0, result, DELTA);
    }

    @Test
    @DisplayName("rejects a null item")
    void rejectsNullItem() {
        assertThrows(IllegalArgumentException.class,
            () -> calculator.calculateFinalPrice(null, 1, List.of()));
    }

    @Test
    @DisplayName("rejects a zero or negative quantity")
    void rejectsNonPositiveQuantity() {
        assertThrows(IllegalArgumentException.class,
            () -> calculator.calculateFinalPrice(item, 0, List.of()));
        assertThrows(IllegalArgumentException.class,
            () -> calculator.calculateFinalPrice(item, -1, List.of()));
    }

    @Test
    @DisplayName("rejects a null discounts list")
    void rejectsNullDiscounts() {
        assertThrows(IllegalArgumentException.class,
            () -> calculator.calculateFinalPrice(item, 1, null));
    }

    @Test
    @DisplayName("averagePricePerUnit divides the final price evenly across quantity")
    void averagePricePerUnitDividesEvenly() {
        List<Discount> discounts = List.of(new FlatAmountDiscount(20.0));
        // 4 units at $50 = $200, minus $20 flat = $180, / 4 units = $45/unit
        double result = calculator.averagePricePerUnit(item, 4, discounts);

        assertEquals(45.0, result, DELTA);
    }
}
