package com.crashcourse.week13.facit;

/** Facit, uppgift 2: raden har fel antal fält. */
public class WrongColumnCountException extends MalformedRecordException {

    public WrongColumnCountException(String message) {
        super(message);
    }

    public WrongColumnCountException(String message, Throwable cause) {
        super(message, cause);
    }
}
