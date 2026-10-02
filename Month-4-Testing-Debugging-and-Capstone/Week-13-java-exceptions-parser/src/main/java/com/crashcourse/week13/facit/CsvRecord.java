package com.crashcourse.week13.facit;

import java.util.Objects;

/** Facit, uppgift 1: CsvRecord med ett femte fält, salary. Se FACIT.md. */
public final class CsvRecord {

    private final String name;
    private final int age;
    private final String email;
    private final String department;
    private final double salary;

    public CsvRecord(String name, int age, String email, String department, double salary) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name must not be blank");
        }
        if (age < 0) {
            throw new IllegalArgumentException("Age must not be negative, got " + age);
        }
        if (email == null || !email.contains("@")) {
            throw new IllegalArgumentException("Email must contain '@', got \"" + email + "\"");
        }
        if (department == null || department.isBlank()) {
            throw new IllegalArgumentException("Department must not be blank");
        }
        // !(salary >= 0) är sant både för negativa tal och för NaN.
        if (!(salary >= 0) || Double.isInfinite(salary)) {
            throw new IllegalArgumentException("Salary must be a non-negative number, got " + salary);
        }
        this.name = name;
        this.age = age;
        this.email = email;
        this.department = department;
        this.salary = salary;
    }

    public String name() {
        return name;
    }

    public int age() {
        return age;
    }

    public String email() {
        return email;
    }

    public String department() {
        return department;
    }

    public double salary() {
        return salary;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (!(o instanceof CsvRecord other)) {
            return false;
        }
        return age == other.age
            && Double.compare(salary, other.salary) == 0
            && name.equals(other.name)
            && email.equals(other.email)
            && department.equals(other.department);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age, email, department, salary);
    }

    @Override
    public String toString() {
        return "CsvRecord{name='%s', age=%d, email='%s', department='%s', salary=%.2f}"
            .formatted(name, age, email, department, salary);
    }
}
