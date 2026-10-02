package com.crashcourse.week17.facit;

/**
 * Thrown when an operation references a member id that isn't on record.
 *
 * <p><b>Unchecked on purpose</b> (extends {@link RuntimeException}, not
 * {@link Exception}): reaching this almost always means the caller passed
 * a wrong or stale id - a usage mistake closer to
 * {@link IllegalArgumentException} than to a routine business outcome the
 * caller must plan a distinct response for. Every caller across this
 * project handles it the same way (report "member not found" and stop),
 * so forcing every intermediate layer to declare or catch it would be
 * ceremony without benefit. Contrast this with {@link
 * ItemNotAvailableException} and {@link BorrowingLimitExceededException}
 * below, which are checked for exactly the opposite reason.
 */
public class MemberNotFoundException extends RuntimeException {

    public MemberNotFoundException(String message) {
        super(message);
    }
}
