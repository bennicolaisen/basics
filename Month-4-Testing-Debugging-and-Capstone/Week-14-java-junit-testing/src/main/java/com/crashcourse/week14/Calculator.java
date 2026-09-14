package com.crashcourse.week14;

/**
 * A small, deliberately simple calculator - the subject under test for this
 * week's JUnit 5 exercises. The behavior is intentionally easy to reason
 * about so the tests, not the arithmetic, are the point.
 */
public class Calculator {

    public double add(double a, double b) {
        return a + b;
    }

    public double subtract(double a, double b) {
        return a - b;
    }

    public double multiply(double a, double b) {
        return a * b;
    }

    public double divide(double a, double b) {
        if (b == 0) {
            throw new ArithmeticException("Division by zero");
        }
        return a / b;
    }

    /**
     * Raises {@code base} to a non-negative integer {@code exponent}.
     * {@code power(x, 0)} is 1 for every {@code x}, matching the usual
     * mathematical convention.
     */
    public double power(double base, int exponent) {
        if (exponent < 0) {
            throw new IllegalArgumentException(
                "Exponent must be non-negative, got " + exponent);
        }
        double result = 1;
        for (int i = 0; i < exponent; i++) {
            result *= base;
        }
        return result;
    }
}
