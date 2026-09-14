package com.crashcourse.week13;

/** One line of a batch that failed to parse: where, and why. */
public final class ParseError {

    private final int lineNumber;
    private final String message;

    public ParseError(int lineNumber, String message) {
        this.lineNumber = lineNumber;
        this.message = message;
    }

    public int lineNumber() {
        return lineNumber;
    }

    public String message() {
        return message;
    }

    @Override
    public String toString() {
        return "line " + lineNumber + ": " + message;
    }
}
