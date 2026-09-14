package com.crashcourse.week14;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.MethodSource;

import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.params.provider.Arguments.arguments;

/**
 * Demonstrates the core JUnit 5 toolkit against {@link Calculator}:
 * {@code @BeforeEach} setup, {@code @DisplayName}, parameterized tests via
 * both {@code @CsvSource} and {@code @MethodSource}, exception testing with
 * {@code assertThrows}, grouped assertions with {@code assertAll}, and
 * {@code @Nested} classes organizing tests by the method under test.
 */
class CalculatorTest {

    private Calculator calculator;

    // Runs before every single @Test (including ones inside @Nested classes)
    // so each test starts from a fresh Calculator - no test can leak state
    // into another one.
    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }

    @Nested
    @DisplayName("add(a, b)")
    class AddTests {

        @ParameterizedTest(name = "{0} + {1} = {2}")
        @CsvSource({
            "2, 3, 5",
            "-2, 3, 1",
            "0, 0, 0",
            "2.5, 2.5, 5.0"
        })
        @DisplayName("adds two numbers correctly across positive, negative, zero, and fractional inputs")
        void addsCorrectly(double a, double b, double expected) {
            assertEquals(expected, calculator.add(a, b));
        }

        @Test
        @DisplayName("addition is commutative")
        void isCommutative() {
            assertAll("a + b should equal b + a for several pairs",
                () -> assertEquals(calculator.add(3, 4), calculator.add(4, 3)),
                () -> assertEquals(calculator.add(-5, 2), calculator.add(2, -5)),
                () -> assertEquals(calculator.add(0, 9), calculator.add(9, 0))
            );
        }
    }

    @Nested
    @DisplayName("subtract(a, b)")
    class SubtractTests {

        @ParameterizedTest(name = "{0} - {1} = {2}")
        @CsvSource({
            "5, 3, 2",
            "3, 5, -2",
            "0, 0, 0",
            "5.5, 0.5, 5.0"
        })
        @DisplayName("subtracts two numbers correctly")
        void subtractsCorrectly(double a, double b, double expected) {
            assertEquals(expected, calculator.subtract(a, b));
        }
    }

    @Nested
    @DisplayName("multiply(a, b)")
    class MultiplyTests {

        @ParameterizedTest(name = "{0} * {1} = {2}")
        @CsvSource({
            "3, 4, 12",
            "-3, 4, -12",
            "0, 100, 0",
            "2.5, 2, 5.0"
        })
        @DisplayName("multiplies two numbers correctly")
        void multipliesCorrectly(double a, double b, double expected) {
            assertEquals(expected, calculator.multiply(a, b));
        }
    }

    @Nested
    @DisplayName("divide(a, b)")
    class DivideTests {

        // @MethodSource is the right tool over @CsvSource whenever the
        // cases are easier to express as real values than as text - here,
        // it also directly returns the already-paired (dividend, divisor,
        // quotient) tuples for readability.
        static Stream<Arguments> divisionCases() {
            return Stream.of(
                arguments(10.0, 2.0, 5.0),
                arguments(9.0, 3.0, 3.0),
                arguments(-10.0, 2.0, -5.0),
                arguments(7.5, 2.5, 3.0)
            );
        }

        @ParameterizedTest(name = "{0} / {1} = {2}")
        @MethodSource("divisionCases")
        @DisplayName("divides two numbers correctly")
        void dividesCorrectly(double a, double b, double expected) {
            assertEquals(expected, calculator.divide(a, b));
        }

        @Test
        @DisplayName("throws ArithmeticException when dividing by zero")
        void throwsOnDivisionByZero() {
            ArithmeticException ex = assertThrows(ArithmeticException.class,
                () -> calculator.divide(5, 0));

            assertEquals("Division by zero", ex.getMessage());
        }
    }

    @Nested
    @DisplayName("power(base, exponent)")
    class PowerTests {

        @ParameterizedTest(name = "{0}^{1} = {2}")
        @CsvSource({
            "2, 0, 1",
            "2, 1, 2",
            "2, 10, 1024",
            "5, 3, 125",
            "-2, 3, -8"
        })
        @DisplayName("raises base to a non-negative integer exponent correctly")
        void raisesToPowerCorrectly(double base, int exponent, double expected) {
            assertEquals(expected, calculator.power(base, exponent));
        }

        @Test
        @DisplayName("throws IllegalArgumentException for a negative exponent")
        void throwsOnNegativeExponent() {
            IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> calculator.power(2, -1));

            assertAll("the message should name the offending exponent",
                () -> assertTrue(ex.getMessage().contains("-1")),
                () -> assertTrue(ex.getMessage().toLowerCase().contains("non-negative"))
            );
        }
    }
}
