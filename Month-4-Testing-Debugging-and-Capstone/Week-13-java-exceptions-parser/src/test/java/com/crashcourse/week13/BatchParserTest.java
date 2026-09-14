package com.crashcourse.week13;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BatchParserTest {

    @Test
    @DisplayName("An empty file parses to zero records and zero errors")
    void emptyFileParsesToNothing(@TempDir Path tempDir) throws IOException {
        Path file = tempDir.resolve("empty.csv");
        Files.writeString(file, "");

        BatchParseResult result = BatchParser.parseFile(file);

        assertTrue(result.records().isEmpty());
        assertTrue(result.errors().isEmpty());
        assertFalse(result.hasErrors());
    }

    @Test
    @DisplayName("A file of only well-formed lines parses every record with no errors")
    void allGoodLinesAllParse(@TempDir Path tempDir) throws IOException {
        Path file = tempDir.resolve("good.csv");
        Files.writeString(file, String.join("\n",
            "Alice,30,alice@example.com,Engineering",
            "Bob,25,bob@example.com,Sales"));

        BatchParseResult result = BatchParser.parseFile(file);

        assertEquals(2, result.records().size());
        assertFalse(result.hasErrors());
    }

    @Test
    @DisplayName("A mix of good and bad lines parses the good ones and reports the bad ones without stopping")
    void mixedGoodAndBadLinesBothSurvive(@TempDir Path tempDir) throws IOException {
        Path file = tempDir.resolve("mixed.csv");
        Files.writeString(file, String.join("\n",
            "Alice,30,alice@example.com,Engineering",  // line 1: good
            "Bob,thirty,bob@example.com,Sales",         // line 2: bad age
            "Carol,40,carol@example.com,Marketing",     // line 3: good
            "Dave,22,dave-example.com,Support",         // line 4: bad email
            "Eve,28,eve@example.com"));                 // line 5: wrong column count

        BatchParseResult result = BatchParser.parseFile(file);

        assertEquals(List.of("Alice", "Carol"),
            result.records().stream().map(CsvRecord::name).toList(),
            "the two well-formed lines should have parsed despite the bad ones around them");

        assertEquals(List.of(2, 4, 5),
            result.errors().stream().map(ParseError::lineNumber).toList(),
            "every bad line should be reported, by its 1-based line number");
    }

    @Test
    @DisplayName("Blank lines are skipped rather than reported as errors")
    void blankLinesAreSkipped(@TempDir Path tempDir) throws IOException {
        Path file = tempDir.resolve("blanks.csv");
        Files.writeString(file, String.join("\n",
            "Alice,30,alice@example.com,Engineering",
            "",
            "Bob,25,bob@example.com,Sales"));

        BatchParseResult result = BatchParser.parseFile(file);

        assertEquals(2, result.records().size());
        assertFalse(result.hasErrors());
    }
}
