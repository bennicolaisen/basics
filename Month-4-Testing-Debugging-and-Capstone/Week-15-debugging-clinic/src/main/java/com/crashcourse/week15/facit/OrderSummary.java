package com.crashcourse.week15.facit;

/**
 * Facit, uppgift 3: "inga rabatterade varutyper" är ett vanligt, giltigt
 * fall, och metoden säger nu uttryckligen vad svaret är då.
 */
public final class OrderSummary {

    public int averageFreeUnitsPerItemType(int totalFreeUnits, int distinctItemTypes) {
        if (distinctItemTypes == 0) {
            return 0;
        }
        return totalFreeUnits / distinctItemTypes;
    }

    public double averageFreeUnitsPerItemType(double totalFreeUnits, double distinctItemTypes) {
        if (distinctItemTypes == 0) {
            return 0.0;
        }
        return totalFreeUnits / distinctItemTypes;
    }
}
