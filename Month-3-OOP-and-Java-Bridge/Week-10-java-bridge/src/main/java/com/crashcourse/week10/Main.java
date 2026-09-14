package com.crashcourse.week10;

/**
 * Entry point: every runnable Java program needs exactly one method shaped
 * like this one somewhere. See the README's Concepts Refresher for what
 * each piece of the signature means.
 */
public class Main {

    public static void main(String[] args) {
        double celsius = 100.0;
        double fahrenheit = Converters.celsiusToFahrenheit(celsius);
        System.out.printf("%.1f C is %.1f F%n", celsius, fahrenheit);

        double km = 42.195; // a marathon
        double miles = Converters.kmToMiles(km);
        System.out.printf("%.3f km is %.3f miles%n", km, miles);

        String sentence = "the quick brown fox jumps over the lazy dog";
        int words = TextUtils.wordCount(sentence);
        System.out.printf("\"%s\" has %d words%n", sentence, words);

        String candidate = "Was it a car or a cat I saw";
        boolean palindrome = TextUtils.isPalindrome(candidate.replace(" ", ""), true);
        System.out.printf("\"%s\" (spaces removed) is a palindrome (ignoring case): %b%n",
                candidate, palindrome);
    }
}
