package com.crashcourse.week17;

/** A library magazine: title and issue number, with a two-week loan period. */
public final class Magazine extends LibraryItem {

    private static final int LOAN_PERIOD_DAYS = 14;

    private final int issueNumber;

    public Magazine(String id, String title, int issueNumber) {
        super(id, title);
        if (issueNumber <= 0) {
            throw new IllegalArgumentException(
                "Issue number must be positive, got " + issueNumber);
        }
        this.issueNumber = issueNumber;
    }

    public int issueNumber() {
        return issueNumber;
    }

    @Override
    public int loanPeriodDays() {
        return LOAN_PERIOD_DAYS;
    }
}
