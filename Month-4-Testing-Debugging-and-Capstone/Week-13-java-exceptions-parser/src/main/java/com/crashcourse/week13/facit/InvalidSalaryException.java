package com.crashcourse.week13.facit;

/** Facit, uppgift 2: lönen är inte ett tal, eller är negativ. */
public class InvalidSalaryException extends MalformedRecordException {

    public InvalidSalaryException(String message) {
        super(message);
    }

    public InvalidSalaryException(String message, Throwable cause) {
        super(message, cause);
    }
}
