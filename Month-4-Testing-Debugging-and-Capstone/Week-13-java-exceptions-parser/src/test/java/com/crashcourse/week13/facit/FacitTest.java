package com.crashcourse.week13.facit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class FacitTest {

    private static final String GOOD = "Ada,36,ada@example.com,Engineering,52000.50";

    // Uppgift 1: salary

    @Test
    void parsesSalary() throws MalformedRecordException {
        CsvRecord record = CsvRecordParser.parseLine(GOOD);
        assertEquals(52000.50, record.salary(), 1e-9);
        assertEquals("Ada", record.name());
    }

    @Test
    void zeroSalaryIsAllowed() throws MalformedRecordException {
        assertEquals(0.0, CsvRecordParser.parseLine("Bo,20,bo@x.se,Sales,0").salary(), 0.0);
    }

    @Test
    void negativeSalaryIsRejected() {
        assertThrows(InvalidSalaryException.class,
            () -> CsvRecordParser.parseLine("Bo,20,bo@x.se,Sales,-1"));
    }

    @Test
    void nonNumericSalaryIsRejected() {
        assertThrows(InvalidSalaryException.class,
            () -> CsvRecordParser.parseLine("Bo,20,bo@x.se,Sales,lots"));
    }

    @Test
    void notANumberSalaryIsRejected() {
        // Double.parseDouble("NaN") lyckas, så NaN måste stoppas separat.
        assertThrows(InvalidSalaryException.class,
            () -> CsvRecordParser.parseLine("Bo,20,bo@x.se,Sales,NaN"));
        assertThrows(InvalidSalaryException.class,
            () -> CsvRecordParser.parseLine("Bo,20,bo@x.se,Sales,Infinity"));
    }

    @Test
    void oldFourFieldFormatIsNowWrong() {
        assertThrows(WrongColumnCountException.class,
            () -> CsvRecordParser.parseLine("Bo,20,bo@x.se,Sales"));
    }

    @Test
    void recordConstructorAlsoGuardsSalary() {
        assertThrows(IllegalArgumentException.class,
            () -> new CsvRecord("Bo", 20, "bo@x.se", "Sales", -5));
    }

    // Uppgift 2: en undantagsklass per kategori

    @Test
    void eachCategoryHasItsOwnException() {
        assertThrows(EmptyLineException.class, () -> CsvRecordParser.parseLine("  "));
        assertThrows(WrongColumnCountException.class, () -> CsvRecordParser.parseLine("a,b"));
        assertThrows(InvalidAgeException.class,
            () -> CsvRecordParser.parseLine("Bo,old,bo@x.se,Sales,1"));
        assertThrows(InvalidAgeException.class,
            () -> CsvRecordParser.parseLine("Bo,-3,bo@x.se,Sales,1"));
        assertThrows(InvalidFieldException.class,
            () -> CsvRecordParser.parseLine("Bo,20,no-at-sign,Sales,1"));
        assertThrows(InvalidFieldException.class,
            () -> CsvRecordParser.parseLine(" ,20,bo@x.se,Sales,1"));
    }

    @Test
    void everyCategoryIsStillAMalformedRecordException() {
        MalformedRecordException e = assertThrows(MalformedRecordException.class,
            () -> CsvRecordParser.parseLine("Bo,old,bo@x.se,Sales,1"));
        assertInstanceOf(InvalidAgeException.class, e);
        assertInstanceOf(NumberFormatException.class, e.getCause());
    }

    // Uppgift 3: filter

    @Test
    void filterKeepsOnlyMatchingRecords(@TempDir Path dir) throws IOException {
        Path file = write(dir, GOOD, "Bo,20,bo@x.se,Sales,30000", "Cy,41,cy@x.se,Engineering,61000");
        BatchParseResult result = BatchParser.parseFile(file, r -> r.department().equals("Engineering"));
        assertEquals(List.of("Ada", "Cy"), result.records().stream().map(CsvRecord::name).toList());
        assertTrue(result.errors().isEmpty());
    }

    @Test
    void filterDoesNotHideMalformedLines(@TempDir Path dir) throws IOException {
        Path file = write(dir, GOOD, "broken line", "Bo,20,bo@x.se,Sales,30000");
        BatchParseResult result = BatchParser.parseFile(file, r -> false);
        assertTrue(result.records().isEmpty());
        assertEquals(1, result.errors().size());
        assertEquals(2, result.errors().get(0).lineNumber());
    }

    // Uppgift 4: rapport

    @Test
    void reportSummarizesSuccessesAndErrors(@TempDir Path dir) throws IOException {
        Path csv = write(dir, GOOD, "broken line", "", "Bo,x,bo@x.se,Sales,1");
        Path report = dir.resolve("report.txt");
        ParseReport.write(BatchParser.parseFile(csv), report);

        List<String> lines = Files.readAllLines(report, StandardCharsets.UTF_8);
        assertEquals("Parse report", lines.get(0));
        assertEquals("Records parsed: 1", lines.get(1));
        assertEquals("Lines failed: 2", lines.get(2));
        assertEquals("Errors:", lines.get(3));
        assertTrue(lines.get(4).startsWith("  line 2: Expected 5"));
        assertTrue(lines.get(5).startsWith("  line 4: Age must be a whole number"));
        assertEquals(6, lines.size());
    }

    @Test
    void reportWithoutErrorsSaysSo() {
        BatchParseResult clean = new BatchParseResult(List.of(), List.of());
        assertEquals(List.of("Parse report", "Records parsed: 0", "Lines failed: 0", "Errors: none"),
            ParseReport.lines(clean));
    }

    // Uppgift 5: strikt läge

    @Test
    void blankLineIsSkippedByDefault(@TempDir Path dir) throws IOException {
        Path file = write(dir, GOOD, "   ", "Bo,20,bo@x.se,Sales,1");
        BatchParseResult result = BatchParser.parseFile(file, false);
        assertEquals(2, result.records().size());
        assertTrue(result.errors().isEmpty());
        assertEquals(result.records(), BatchParser.parseFile(file).records());
    }

    @Test
    void blankLineIsAnErrorInStrictMode(@TempDir Path dir) throws IOException {
        Path file = write(dir, GOOD, "   ", "Bo,20,bo@x.se,Sales,1");
        BatchParseResult result = BatchParser.parseFile(file, true);
        assertEquals(2, result.records().size());
        assertEquals(1, result.errors().size());
        assertEquals(2, result.errors().get(0).lineNumber());
        assertEquals("Line is blank", result.errors().get(0).message());
    }

    private static Path write(Path dir, String... lines) throws IOException {
        Path file = dir.resolve("people.csv");
        Files.write(file, List.of(lines), StandardCharsets.UTF_8);
        return file;
    }
}
