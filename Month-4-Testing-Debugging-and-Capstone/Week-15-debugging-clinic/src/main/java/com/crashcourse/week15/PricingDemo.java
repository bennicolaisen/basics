package com.crashcourse.week15;

import java.util.List;

/**
 * A runnable entry point purely so this project has something to launch
 * under a debugger - set a breakpoint inside {@link PriceCalculator} and
 * step through a real call chain, per this week's README.
 */
public final class PricingDemo {

    public static void main(String[] args) {
        Item headphones = new Item("SKU-100", "Wireless Headphones", 80.00);

        List<Discount> discounts = List.of(
            new PercentageDiscount(10),
            new FlatAmountDiscount(5.00),
            new BuyOneGetOneDiscount()
        );

        PriceCalculator calculator = new PriceCalculator();
        int quantity = 3;

        double finalPrice = calculator.calculateFinalPrice(headphones, quantity, discounts);
        double perUnit = calculator.averagePricePerUnit(headphones, quantity, discounts);

        System.out.println("Item: " + headphones);
        System.out.println("Quantity: " + quantity);
        for (Discount discount : discounts) {
            System.out.println("Discount applied: " + discount.description());
        }
        System.out.printf("Final price: $%.2f%n", finalPrice);
        System.out.printf("Average price per unit: $%.2f%n", perUnit);
    }
}
