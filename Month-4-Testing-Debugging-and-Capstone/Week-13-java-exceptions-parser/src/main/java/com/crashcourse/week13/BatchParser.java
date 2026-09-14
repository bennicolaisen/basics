package com.crashcourse.week13;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/**
 * Parses an entire CSV file, one line at a time, without letting a single
 * malformed line abort the whole batch.
 *
 * <p>This is the resilient counterpart to {@link CsvRecordParser}'s
 * fail-fast, single-line parsing: each line is attempted independently, a
 * {@link MalformedRecordException} on one line is caught and recorded as a
 * {@link ParseError} (with its 1-based line number), and parsing continues
 * to the next line. The caller gets both the records that succeeded and a
 * full account of what failed and why - nothing is silently dropped, and
 * nothing is silently skipped.
 */
public final class BatchParser {

    private BatchParser() {
        // utility class: no instances
    }

    public static BatchParseResult parseFile(Path path) throws IOException {
        List<CsvRecord> records = new ArrayList<>();
        List<ParseError> errors = new ArrayList<>();

        // try-with-resources guarantees the reader is closed even if a line
        // throws partway through the file - equivalent to a manual
        // try/finally that closes the reader, without having to write it.
        try (BufferedReader reader = Files.newBufferedReader(path)) {
            String line;
            int lineNumber = 0;
            while ((line = reader.readLine()) != null) {
                lineNumber++;
                if (line.isBlank()) {
                    continue; // a blank line is not data; skip it rather than report it
                }
                try {
                    records.add(CsvRecordParser.parseLine(line));
                } catch (MalformedRecordException e) {
                    errors.add(new ParseError(lineNumber, e.getMessage()));
                }
            }
        }

        return new BatchParseResult(records, errors);
    }

    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            System.err.println("Usage: java -jar week13.jar <path-to-csv>");
            return;
        }

        BatchParseResult result = parseFile(Path.of(args[0]));

        System.out.println(result.records().size() + " record(s) parsed successfully:");
        for (CsvRecord record : result.records()) {
            System.out.println("  " + record);
        }

        if (result.hasErrors()) {
            System.out.println(result.errors().size() + " line(s) failed to parse:");
            for (ParseError error : result.errors()) {
                System.out.println("  " + error);
            }
        }
    }
}
