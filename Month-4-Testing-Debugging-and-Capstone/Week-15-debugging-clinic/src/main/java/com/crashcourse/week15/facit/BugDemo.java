package com.crashcourse.week15.facit;

/**
 * Facit, uppgift 1, 2 och 4: kör buggen och se vad som händer.
 *
 * <pre>
 * mvn -q compile
 * java -cp target/classes com.crashcourse.week15.facit.BugDemo int
 * java -cp target/classes com.crashcourse.week15.facit.BugDemo double
 * java -cp target/classes com.crashcourse.week15.facit.BugDemo fixed
 * </pre>
 */
public final class BugDemo {

    private BugDemo() {
    }

    public static void main(String[] args) {
        String variant = args.length > 0 ? args[0] : "int";
        int totalFreeUnits = 0;
        int distinctItemTypes = 0; // en order utan några BOGO-rabatter

        switch (variant) {
            case "int" -> {
                BuggyOrderSummary summary = new BuggyOrderSummary();
                int average = summary.averageFreeUnitsPerItemType(totalFreeUnits, distinctItemTypes);
                System.out.println("Average free units per item type: " + average);
            }
            case "double" -> {
                BuggyOrderSummary summary = new BuggyOrderSummary();
                double average = summary.averageFreeUnitsPerItemType(
                    (double) totalFreeUnits, (double) distinctItemTypes);
                // Inget kastas. NaN följer med i nästa uträkning ...
                double savedPerItemType = average * 80.00;
                // ... och syns först här, långt från där det gick fel.
                System.out.printf("Saved per item type: $%.2f%n", savedPerItemType);
            }
            case "fixed" -> {
                OrderSummary summary = new OrderSummary();
                int average = summary.averageFreeUnitsPerItemType(totalFreeUnits, distinctItemTypes);
                System.out.println("Average free units per item type: " + average);
            }
            default -> System.out.println("Usage: BugDemo [int|double|fixed]");
        }
    }
}
