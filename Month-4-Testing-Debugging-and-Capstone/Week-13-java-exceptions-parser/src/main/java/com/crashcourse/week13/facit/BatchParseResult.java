package com.crashcourse.week13.facit;

import java.util.List;

/**
 * The outcome of parsing an entire file: every record that parsed
 * successfully, and every line that did not, with a reason - side by side,
 * neither one hidden by the other.
 */
public final class BatchParseResult {

    private final List<CsvRecord> records;
    private final List<ParseError> errors;

    public BatchParseResult(List<CsvRecord> records, List<ParseError> errors) {
        this.records = List.copyOf(records);
        this.errors = List.copyOf(errors);
    }

    public List<CsvRecord> records() {
        return records;
    }

    public List<ParseError> errors() {
        return errors;
    }

    public boolean hasErrors() {
        return !errors.isEmpty();
    }
}
