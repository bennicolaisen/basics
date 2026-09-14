package com.crashcourse.week13;

import java.util.Objects;

/**
 * An immutable, validated record parsed from one line of CSV input.
 *
 * <p>Validation lives in the constructor so that a {@code CsvRecord}
 * instance is <em>always</em> in a valid state - there is no way to obtain
 * one whose age is negative or whose email is missing an "@". The
 * constructor throws the unchecked {@link IllegalArgumentException} because
 * these checks guard a programming contract on this class itself (any code
 * anywhere could try to construct one), whereas {@link CsvRecordParser}
 * deals with the separate, checked concern of a malformed line of external
 * input - see {@link MalformedRecordException} for that distinction.
 */
public final class CsvRecord {

    private final String name;
    private final int age;
    private final String email;
    private final String department;

    public CsvRecord(String name, int age, String email, String department) {
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
        this.name = name;
        this.age = age;
        this.email = email;
        this.department = department;
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

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (!(o instanceof CsvRecord other)) {
            return false;
        }
        return age == other.age
            && name.equals(other.name)
            && email.equals(other.email)
            && department.equals(other.department);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age, email, department);
    }

    @Override
    public String toString() {
        return "CsvRecord{name='%s', age=%d, email='%s', department='%s'}"
            .formatted(name, age, email, department);
    }
}
