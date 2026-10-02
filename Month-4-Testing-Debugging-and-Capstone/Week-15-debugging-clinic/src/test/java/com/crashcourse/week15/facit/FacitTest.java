package com.crashcourse.week15.facit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.crashcourse.week15.BuyOneGetOneDiscount;
import com.crashcourse.week15.Discount;
import com.crashcourse.week15.FlatAmountDiscount;
import com.crashcourse.week15.Item;
import com.crashcourse.week15.PercentageDiscount;
import com.crashcourse.week15.PriceCalculator;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import org.junit.jupiter.api.Test;

class FacitTest {

    // Uppgift 1 och 2: buggen kastar, och översta raden i stackspåret är metoden med divisionen.

    @Test
    void buggyIntVersionThrowsDivideByZero() {
        ArithmeticException e = assertThrows(ArithmeticException.class,
            () -> new BuggyOrderSummary().averageFreeUnitsPerItemType(0, 0));
        assertEquals("/ by zero", e.getMessage());
        StackTraceElement top = e.getStackTrace()[0];
        assertEquals(BuggyOrderSummary.class.getName(), top.getClassName());
        assertEquals("averageFreeUnitsPerItemType", top.getMethodName());
    }

    @Test
    void demoCrashesWithTheSameException() {
        assertThrows(ArithmeticException.class, () -> BugDemo.main(new String[] {"int"}));
    }

    // Uppgift 3: rättelsen

    @Test
    void fixedVersionReturnsZeroForNoItemTypes() {
        assertEquals(0, new OrderSummary().averageFreeUnitsPerItemType(0, 0));
        assertEquals(0, new OrderSummary().averageFreeUnitsPerItemType(7, 0));
    }

    @Test
    void fixedVersionStillDividesNormally() {
        assertEquals(2, new OrderSummary().averageFreeUnitsPerItemType(6, 3));
    }

    @Test
    void integerDivisionTruncates() {
        // Ett annat problem med int: 5 / 2 är 2, inte 2,5.
        assertEquals(2, new OrderSummary().averageFreeUnitsPerItemType(5, 2));
        assertEquals(2.5, new OrderSummary().averageFreeUnitsPerItemType(5.0, 2.0));
    }

    // Uppgift 4: double kastar inte, utan ger tyst ett trasigt värde.

    @Test
    void buggyDoubleVersionGivesNaNOrInfinity() {
        BuggyOrderSummary summary = new BuggyOrderSummary();
        assertTrue(Double.isNaN(summary.averageFreeUnitsPerItemType(0.0, 0.0)));
        assertEquals(Double.POSITIVE_INFINITY, summary.averageFreeUnitsPerItemType(5.0, 0.0));
    }

    @Test
    void nanTravelsDownstreamWithoutAnyException() {
        String output = captureOutput(() -> BugDemo.main(new String[] {"double"}));
        assertEquals("Saved per item type: $NaN", output.strip());
    }

    @Test
    void fixedDoubleVersionReturnsZero() {
        assertEquals(0.0, new OrderSummary().averageFreeUnitsPerItemType(0.0, 0.0));
    }

    @Test
    void fixedDemoPrintsZero() {
        String output = captureOutput(() -> BugDemo.main(new String[] {"fixed"}));
        assertEquals("Average free units per item type: 0", output.strip());
    }

    // Uppgift 5: värdena du ska se i debuggern, ett steg i taget.

    @Test
    void runningTotalStepByStep() {
        Item headphones = new Item("SKU-100", "Wireless Headphones", 80.00);
        int quantity = 3;
        double total = headphones.basePrice() * quantity;
        assertEquals(240.0, total, 1e-9);

        total = new PercentageDiscount(10).applyTo(total, headphones, quantity);
        assertEquals(216.0, total, 1e-9);

        total = new FlatAmountDiscount(5.00).applyTo(total, headphones, quantity);
        assertEquals(211.0, total, 1e-9);

        total = new BuyOneGetOneDiscount().applyTo(total, headphones, quantity);
        assertEquals(131.0, total, 1e-9);

        List<Discount> discounts = List.of(
            new PercentageDiscount(10), new FlatAmountDiscount(5.00), new BuyOneGetOneDiscount());
        assertEquals(131.0, new PriceCalculator().calculateFinalPrice(headphones, quantity, discounts), 1e-9);
    }

    private static String captureOutput(Runnable action) {
        PrintStream original = System.out;
        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        System.setOut(new PrintStream(buffer, true, StandardCharsets.UTF_8));
        try {
            action.run();
        } finally {
            System.setOut(original);
        }
        return buffer.toString(StandardCharsets.UTF_8);
    }
}
