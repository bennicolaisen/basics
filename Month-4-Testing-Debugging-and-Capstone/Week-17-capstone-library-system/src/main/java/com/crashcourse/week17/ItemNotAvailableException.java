package com.crashcourse.week17;

/**
 * Thrown when a checkout cannot proceed because the requested item either
 * doesn't exist in the catalog, or exists but is currently checked out to
 * someone else.
 *
 * <p><b>Checked on purpose</b> (extends {@link Exception}, not {@link
 * RuntimeException}) - matching the reasoning from Week 13: this is a
 * routine, expected outcome of calling {@link Library#checkOut}, not a
 * programming mistake, and the caller (a UI, a CLI, another service)
 * genuinely has to decide how to respond - offer a hold, suggest another
 * copy, or simply report it. Making it checked forces that decision to be
 * made explicitly at every call site, rather than risking it going
 * unhandled the first time it actually happens.
 */
public class ItemNotAvailableException extends Exception {

    public ItemNotAvailableException(String message) {
        super(message);
    }
}
