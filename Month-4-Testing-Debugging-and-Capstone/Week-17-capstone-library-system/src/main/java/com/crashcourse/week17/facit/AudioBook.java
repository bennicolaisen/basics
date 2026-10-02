package com.crashcourse.week17.facit;

/**
 * Facit, uppgift 1: en fjärde sorts LibraryItem. Ingen annan klass behövde
 * ändras för att den skulle gå att låna, lämna tillbaka och förlänga.
 */
public final class AudioBook extends LibraryItem {

    private static final int LOAN_PERIOD_DAYS = 14;

    private final String narrator;
    private final int durationMinutes;

    public AudioBook(String id, String title, String narrator, int durationMinutes) {
        super(id, title);
        if (narrator == null || narrator.isBlank()) {
            throw new IllegalArgumentException("Narrator must not be blank");
        }
        if (durationMinutes <= 0) {
            throw new IllegalArgumentException(
                "Duration minutes must be positive, got " + durationMinutes);
        }
        this.narrator = narrator;
        this.durationMinutes = durationMinutes;
    }

    public String narrator() {
        return narrator;
    }

    public int durationMinutes() {
        return durationMinutes;
    }

    @Override
    public int loanPeriodDays() {
        return LOAN_PERIOD_DAYS;
    }
}
