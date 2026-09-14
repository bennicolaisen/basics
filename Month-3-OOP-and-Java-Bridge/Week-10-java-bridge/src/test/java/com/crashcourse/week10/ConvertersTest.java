package com.crashcourse.week10;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class ConvertersTest {

    private static final double DELTA = 1e-9;

    @Test
    void celsiusToFahrenheitFreezingPoint() {
        assertEquals(32.0, Converters.celsiusToFahrenheit(0), DELTA);
    }

    @Test
    void celsiusToFahrenheitBoilingPoint() {
        assertEquals(212.0, Converters.celsiusToFahrenheit(100), DELTA);
    }

    @Test
    void fahrenheitToCelsiusRoundTrips() {
        double original = 98.6;
        double celsius = Converters.fahrenheitToCelsius(original);
        double back = Converters.celsiusToFahrenheit(celsius);
        assertEquals(original, back, DELTA);
    }

    @Test
    void kmToMilesKnownValue() {
        assertEquals(1.0, Converters.kmToMiles(1.609344), DELTA);
    }

    @Test
    void milesToKmKnownValue() {
        assertEquals(1.609344, Converters.milesToKm(1.0), DELTA);
    }

    @Test
    void kmToMilesAndBackRoundTrips() {
        double original = 42.195;
        double miles = Converters.kmToMiles(original);
        double back = Converters.milesToKm(miles);
        assertEquals(original, back, DELTA);
    }
}
