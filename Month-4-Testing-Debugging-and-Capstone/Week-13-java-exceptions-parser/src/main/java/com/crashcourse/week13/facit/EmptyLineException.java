package com.crashcourse.week13.facit;

/** Facit, uppgift 2: raden är tom. */
public class EmptyLineException extends MalformedRecordException {

    public EmptyLineException(String message) {
        super(message);
    }

    public EmptyLineException(String message, Throwable cause) {
        super(message, cause);
    }
}
