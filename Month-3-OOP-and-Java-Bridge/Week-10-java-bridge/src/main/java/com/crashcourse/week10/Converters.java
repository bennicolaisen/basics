package com.crashcourse.week10;

/**
 * Static unit-conversion methods — a direct Java port of the Python
 * conversion functions from Month 1, Week 1.
 *
 * <p>Every method here is {@code static}: it belongs to the class itself,
 * not to any instance of it, exactly like a plain Python function did.
 * There's no state to bundle with these — no object needs creating just to
 * call {@code celsiusToFahrenheit(100)}.
 */
public final class Converters {

    private static final double KM_PER_MILE = 1.609344;

    // No instances of this class make sense — it's a bundle of static
    // methods, not a thing with state. A private constructor prevents
    // `new Converters()` from compiling.
    private Converters() {
    }

    public static double celsiusToFahrenheit(double celsius) {
        return celsius * 9.0 / 5.0 + 32.0;
    }

    public static double fahrenheitToCelsius(double fahrenheit) {
        return (fahrenheit - 32.0) * 5.0 / 9.0;
    }

    public static double kmToMiles(double km) {
        return km / KM_PER_MILE;
    }

    public static double milesToKm(double miles) {
        return miles * KM_PER_MILE;
    }
}
