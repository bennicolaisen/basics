package com.crashcourse.week13.facit;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Predicate;

/**
 * Facit: BatchParser med filter (uppgift 3) och strikt läge för tomma
 * rader (uppgift 5). Alla varianter av parseFile anropar samma metod längst
 * ned, så logiken finns på ett enda ställe.
 */
public final class BatchParser {

    private BatchParser() {
        // utility class: no instances
    }

    /** Som veckans original: alla rader, tomma rader hoppas över. */
    public static BatchParseResult parseFile(Path path) throws IOException {
        return parseFile(path, record -> true, false);
    }

    /** Uppgift 3: behåll bara poster som filtret godkänner. */
    public static BatchParseResult parseFile(Path path, Predicate<CsvRecord> filter) throws IOException {
        return parseFile(path, filter, false);
    }

    /** Uppgift 5: med strict = true räknas en tom rad som ett fel. */
    public static BatchParseResult parseFile(Path path, boolean strict) throws IOException {
        return parseFile(path, record -> true, strict);
    }

    public static BatchParseResult parseFile(Path path, Predicate<CsvRecord> filter, boolean strict)
            throws IOException {
        if (filter == null) {
            throw new IllegalArgumentException("filter must not be null");
        }
        List<CsvRecord> records = new ArrayList<>();
        List<ParseError> errors = new ArrayList<>();

        try (BufferedReader reader = Files.newBufferedReader(path)) {
            String line;
            int lineNumber = 0;
            while ((line = reader.readLine()) != null) {
                lineNumber++;
                if (line.isBlank()) {
                    if (strict) {
                        errors.add(new ParseError(lineNumber, "Line is blank"));
                    }
                    continue;
                }
                try {
                    CsvRecord record = CsvRecordParser.parseLine(line);
                    // Filtret används bara på rader som gick att läsa. En
                    // trasig rad är fortfarande ett fel, vad filtret än säger.
                    if (filter.test(record)) {
                        records.add(record);
                    }
                } catch (MalformedRecordException e) {
                    errors.add(new ParseError(lineNumber, e.getMessage()));
                }
            }
        }

        return new BatchParseResult(records, errors);
    }
}
