package com.crashcourse.week13.facit;

/**
 * Facit: parsar en rad med fem fält, name,age,email,department,salary
 * (uppgift 1), och kastar en underklass till MalformedRecordException per
 * felkategori (uppgift 2).
 */
public final class CsvRecordParser {

    private static final int EXPECTED_FIELDS = 5;

    private CsvRecordParser() {
        // utility class: no instances
    }

    public static CsvRecord parseLine(String line) throws MalformedRecordException {
        if (line == null || line.isBlank()) {
            throw new EmptyLineException("Line is empty");
        }

        String[] parts = line.split(",", -1);
        if (parts.length != EXPECTED_FIELDS) {
            throw new WrongColumnCountException(
                "Expected %d comma-separated fields (name,age,email,department,salary) but found %d in line: \"%s\""
                    .formatted(EXPECTED_FIELDS, parts.length, line));
        }

        String name = parts[0].trim();
        String rawAge = parts[1].trim();
        String email = parts[2].trim();
        String department = parts[3].trim();
        String rawSalary = parts[4].trim();

        int age;
        try {
            age = Integer.parseInt(rawAge);
        } catch (NumberFormatException e) {
            throw new InvalidAgeException(
                "Age must be a whole number, got \"%s\" in line: \"%s\"".formatted(rawAge, line), e);
        }
        if (age < 0) {
            throw new InvalidAgeException(
                "Age must not be negative, got %d in line: \"%s\"".formatted(age, line));
        }

        double salary;
        try {
            salary = Double.parseDouble(rawSalary);
        } catch (NumberFormatException e) {
            throw new InvalidSalaryException(
                "Salary must be a number, got \"%s\" in line: \"%s\"".formatted(rawSalary, line), e);
        }
        if (!(salary >= 0) || Double.isInfinite(salary)) {
            throw new InvalidSalaryException(
                "Salary must be a non-negative number, got \"%s\" in line: \"%s\"".formatted(rawSalary, line));
        }

        try {
            return new CsvRecord(name, age, email, department, salary);
        } catch (IllegalArgumentException e) {
            // Ålder och lön är redan kontrollerade, så det som återstår är
            // namn, e-post och avdelning.
            throw new InvalidFieldException(e.getMessage() + " in line: \"" + line + "\"", e);
        }
    }
}
