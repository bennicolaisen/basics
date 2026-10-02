package com.crashcourse.week15.facit;

/**
 * Facit, uppgift 1 och 4: buggen från fallstudien, med flit. Rätta
 * versionen finns i {@link OrderSummary}. Se FACIT.md.
 */
public final class BuggyOrderSummary {

    /** Uppgift 1: kastar ArithmeticException när distinctItemTypes är 0. */
    public int averageFreeUnitsPerItemType(int totalFreeUnits, int distinctItemTypes) {
        return totalFreeUnits / distinctItemTypes;
    }

    /** Uppgift 4: samma bugg med double. Kastar aldrig, utan ger NaN eller Infinity. */
    public double averageFreeUnitsPerItemType(double totalFreeUnits, double distinctItemTypes) {
        return totalFreeUnits / distinctItemTypes;
    }
}
