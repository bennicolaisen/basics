package com.crashcourse.week13.facit;

/**
 * Facit: basklassen för alla fel på en rad. Underklasserna (uppgift 2)
 * talar om vilken sorts fel det var; den som inte bryr sig fångar bara
 * den här.
 */
public class MalformedRecordException extends Exception {

    public MalformedRecordException(String message) {
        super(message);
    }

    public MalformedRecordException(String message, Throwable cause) {
        super(message, cause);
    }
}
