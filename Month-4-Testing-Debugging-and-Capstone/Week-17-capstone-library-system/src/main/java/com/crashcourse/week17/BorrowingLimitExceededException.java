package com.crashcourse.week17;

/**
 * Thrown when a member has already reached their borrowing limit and
 * tries to check out another item.
 *
 * <p><b>Checked on purpose</b>, for the same reason as {@link
 * ItemNotAvailableException}: this is an entirely ordinary outcome of
 * normal library use, not a bug, and a caller needs to decide how to
 * respond (prompt the member to return something first, deny the
 * checkout outright, queue it, etc.). The compiler making sure that
 * decision can't be silently skipped is the entire value of a checked
 * exception here.
 */
public class BorrowingLimitExceededException extends Exception {

    public BorrowingLimitExceededException(String message) {
        super(message);
    }
}
