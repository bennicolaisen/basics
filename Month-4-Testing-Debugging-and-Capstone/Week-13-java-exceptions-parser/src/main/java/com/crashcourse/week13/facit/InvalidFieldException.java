package com.crashcourse.week13.facit;

/** Facit, uppgift 2: namn, e-post eller avdelning är ogiltig. */
public class InvalidFieldException extends MalformedRecordException {

    public InvalidFieldException(String message) {
        super(message);
    }

    public InvalidFieldException(String message, Throwable cause) {
        super(message, cause);
    }
}
