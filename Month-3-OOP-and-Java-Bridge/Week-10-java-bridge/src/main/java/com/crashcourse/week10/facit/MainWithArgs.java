package com.crashcourse.week10.facit;

import com.crashcourse.week10.Converters;

/**
 * Facit, uppgift 5: läs temperaturen från {@code args[0]}.
 *
 * <pre>
 * mvn -q compile
 * java -cp target/classes com.crashcourse.week10.facit.MainWithArgs 21.5
 * </pre>
 */
public class MainWithArgs {

    public static void main(String[] args) {
        System.out.println(describe(args));
    }

    /** All logik ligger här, så att den kan testas utan att starta ett program. */
    static String describe(String[] args) {
        if (args.length == 0) {
            return "Usage: MainWithArgs <degrees Celsius>";
        }
        try {
            double celsius = Double.parseDouble(args[0]);
            return String.format("%.1f C is %.1f F", celsius, Converters.celsiusToFahrenheit(celsius));
        } catch (NumberFormatException e) {
            return "Not a number: " + args[0];
        }
    }
}
