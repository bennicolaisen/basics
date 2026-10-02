package com.crashcourse.week10.facit;

import com.crashcourse.week10.Converters;

/**
 * Facit, uppgift 1: Kelvin. Se FACIT.md.
 *
 * <p>{@code Converters} är {@code final} och har en privat konstruktor, så
 * det går inte att ärva från den. Facit lägger därför de nya metoderna i en
 * egen klass; i ett riktigt projekt skulle de stå direkt i {@code Converters}.
 */
public final class ConvertersFacit {

    /** 0 K, den absoluta nollpunkten, uttryckt i Fahrenheit. */
    public static final double ABSOLUTE_ZERO_FAHRENHEIT = -459.67;

    private static final double KELVIN_AT_ZERO_CELSIUS = 273.15;

    private ConvertersFacit() {
    }

    public static double fahrenheitToKelvin(double fahrenheit) {
        if (fahrenheit < ABSOLUTE_ZERO_FAHRENHEIT) {
            throw new IllegalArgumentException("below absolute zero: " + fahrenheit + " F");
        }
        return Converters.fahrenheitToCelsius(fahrenheit) + KELVIN_AT_ZERO_CELSIUS;
    }

    public static double kelvinToFahrenheit(double kelvin) {
        if (kelvin < 0) {
            throw new IllegalArgumentException("below absolute zero: " + kelvin + " K");
        }
        return Converters.celsiusToFahrenheit(kelvin - KELVIN_AT_ZERO_CELSIUS);
    }
}
