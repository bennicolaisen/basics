package com.crashcourse.week14.facit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.params.provider.Arguments.arguments;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;

class FacitTest {

    private Calculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }

    @Nested
    @DisplayName("Uppgift 1: sqrt(x), i den ordning testerna skrevs")
    class SqrtTests {

        // Steg 1: första testet. Det kompilerade inte förrän sqrt fanns.
        @Test
        @DisplayName("sqrt(9) is 3")
        void squareRootOfNine() {
            assertEquals(3.0, calculator.sqrt(9));
        }

        // Steg 2: andra testet. Det föll tills kontrollen av negativa tal fanns.
        @Test
        @DisplayName("sqrt of a negative number throws")
        void negativeInputThrows() {
            IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> calculator.sqrt(-4));
            assertTrue(ex.getMessage().contains("-4"));
        }

        // Steg 3: fler fall när grunden fungerade, bland annat gränsfallet 0.
        @ParameterizedTest(name = "sqrt({0}) = {1}")
        @CsvSource({"0, 0", "1, 1", "2.25, 1.5", "1e6, 1000"})
        void moreCases(double x, double expected) {
            assertEquals(expected, calculator.sqrt(x), 1e-12);
        }
    }

    @Nested
    @DisplayName("Uppgift 2 och 3: power(base, exponent)")
    class PowerTests {

        // Uppgift 2: argumenten byggs med en loop. 2^0 till 2^62, och
        // förväntat värde räknas ut med heltal (1L << n), som är exakt.
        static Stream<Arguments> powersOfTwo() {
            List<Arguments> cases = new ArrayList<>();
            for (int exponent = 0; exponent <= 62; exponent += 2) {
                cases.add(arguments(exponent, (double) (1L << exponent)));
            }
            return cases.stream();
        }

        @ParameterizedTest(name = "2^{0} = {1}")
        @MethodSource("powersOfTwo")
        void largePowersOfTwo(int exponent, double expected) {
            assertEquals(expected, calculator.power(2, exponent));
        }

        // Uppgift 3: @ValueSource ger ett värde per körning; det förväntade
        // värdet räknas ut i testet.
        @ParameterizedTest(name = "2^{0}")
        @ValueSource(ints = {0, 1, 2, 3, 8, 16, 31, 100})
        void matchesMathPow(int exponent) {
            assertEquals(Math.pow(2, exponent), calculator.power(2, exponent));
        }

        // Uppgift 4: veckans egna power-fall, oförändrade. De passerar även
        // när loopen är utbytt mot Math.pow.
        @ParameterizedTest(name = "{0}^{1} = {2}")
        @CsvSource({"2, 0, 1", "2, 1, 2", "2, 10, 1024", "5, 3, 125", "-2, 3, -8"})
        void originalCasesStillPass(double base, int exponent, double expected) {
            assertEquals(expected, calculator.power(base, exponent));
        }

        @Test
        void negativeExponentStillThrows() {
            assertThrows(IllegalArgumentException.class, () -> calculator.power(2, -1));
        }
    }

    // Uppgift 5: ett test märkt som långsamt. Hoppa över det med
    //   mvn test -DexcludedGroups=slow
    // och kör bara sådana tester med
    //   mvn test -Dgroups=slow
    @Test
    @Tag("slow")
    @DisplayName("Uppgift 5: ett 'långsamt' test (märkt med @Tag)")
    void manyAdditions() {
        double total = 0;
        for (int i = 1; i <= 1_000_000; i++) {
            total = calculator.add(total, 1);
        }
        assertEquals(1_000_000.0, total);
    }
}
