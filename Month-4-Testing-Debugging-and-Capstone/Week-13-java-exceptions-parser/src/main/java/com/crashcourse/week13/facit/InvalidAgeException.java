package com.crashcourse.week13.facit;

/** Facit, uppgift 2: åldern är inte ett heltal, eller är negativ. */
public class InvalidAgeException extends MalformedRecordException {

    public InvalidAgeException(String message) {
        super(message);
    }

    public InvalidAgeException(String message, Throwable cause) {
        super(message, cause);
    }
}
