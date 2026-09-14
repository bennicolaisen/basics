package com.crashcourse.week17;

/** A library DVD: title and runtime, with a one-week loan period. */
public final class DVD extends LibraryItem {

    private static final int LOAN_PERIOD_DAYS = 7;

    private final int runtimeMinutes;

    public DVD(String id, String title, int runtimeMinutes) {
        super(id, title);
        if (runtimeMinutes <= 0) {
            throw new IllegalArgumentException(
                "Runtime minutes must be positive, got " + runtimeMinutes);
        }
        this.runtimeMinutes = runtimeMinutes;
    }

    public int runtimeMinutes() {
        return runtimeMinutes;
    }

    @Override
    public int loanPeriodDays() {
        return LOAN_PERIOD_DAYS;
    }
}
