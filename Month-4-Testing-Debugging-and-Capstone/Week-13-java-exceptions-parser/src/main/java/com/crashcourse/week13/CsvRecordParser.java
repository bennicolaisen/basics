package com.crashcourse.week13;

/**
 * Parses a single line of CSV input into a {@link CsvRecord}, failing fast.
 *
 * <p>Expected format: {@code name,age,email,department} - exactly four
 * comma-separated fields, whitespace around each field is trimmed away.
 *
 * <p>This class deliberately does the opposite of {@link BatchParser}: one
 * bad line means one thrown {@link MalformedRecordException}, immediately,
 * naming exactly what was wrong. That is the right behavior when a single
 * record is being parsed in isolation and the caller needs to know right
 * away - "collect and continue" only makes sense once you are processing a
 * whole file of many records, which is what {@link BatchParser} is for.
 */
public final class CsvRecordParser {

    private static final int EXPECTED_FIELDS = 4;

    private CsvRecordParser() {
        // utility class: no instances
    }

    public static CsvRecord parseLine(String line) throws MalformedRecordException {
        if (line == null || line.isBlank()) {
            throw new MalformedRecordException("Line is empty");
        }

        String[] parts = line.split(",", -1);
        if (parts.length != EXPECTED_FIELDS) {
            throw new MalformedRecordException(
                "Expected %d comma-separated fields (name,age,email,department) but found %d in line: \"%s\""
                    .formatted(EXPECTED_FIELDS, parts.length, line));
        }

        String name = parts[0].trim();
        String rawAge = parts[1].trim();
        String email = parts[2].trim();
        String department = parts[3].trim();

        int age;
        try {
            age = Integer.parseInt(rawAge);
        } catch (NumberFormatException e) {
            throw new MalformedRecordException(
                "Age must be a whole number, got \"%s\" in line: \"%s\"".formatted(rawAge, line));
        }

        try {
            return new CsvRecord(name, age, email, department);
        } catch (IllegalArgumentException e) {
            // Re-thrown as the checked MalformedRecordException: from here on,
            // this is a malformed-input problem, not a raw IllegalArgumentException
            // the caller has to know the internals of CsvRecord to expect.
            throw new MalformedRecordException(e.getMessage() + " in line: \"" + line + "\"", e);
        }
    }
}
