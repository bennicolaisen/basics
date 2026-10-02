package com.crashcourse.week14.facit;

/**
 * Facit: Calculator med sqrt (uppgift 1) och power omskriven med Math.pow
 * (uppgift 4). Övriga metoder är oförändrade. Se FACIT.md.
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

    /** Uppgift 4: samma beteende som loopen, men med Math.pow. */
    public double power(double base, int exponent) {
        if (exponent < 0) {
            throw new IllegalArgumentException(
                "Exponent must be non-negative, got " + exponent);
        }
        return Math.pow(base, exponent);
    }

    /** Uppgift 1: kvadratroten, framtagen med TDD. */
    public double sqrt(double x) {
        if (x < 0) {
            throw new IllegalArgumentException(
                "Cannot take the square root of a negative number, got " + x);
        }
        return Math.sqrt(x);
    }
}
