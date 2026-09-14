package com.crashcourse.week13;

/**
 * Signals that a single line of CSV input could not be turned into a
 * {@link CsvRecord}.
 *
 * <p>This is a <em>checked</em> exception on purpose. A malformed line is an
 * entirely expected outcome of reading data that came from outside the
 * program (a file on disk, possibly hand-edited or produced by another
 * tool) - not a programming mistake. Making it checked forces every caller
 * of {@link CsvRecordParser#parseLine(String)} to decide, at compile time,
 * what happens when a line is bad: propagate it, wrap it, or catch it and
 * keep going. {@link BatchParser} is exactly that decision made concrete -
 * it catches this exception per line so that one malformed record does not
 * abort an entire file.
 */
public class MalformedRecordException extends Exception {

    public MalformedRecordException(String message) {
        super(message);
    }

    public MalformedRecordException(String message, Throwable cause) {
        super(message, cause);
    }
}
