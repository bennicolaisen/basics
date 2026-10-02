package com.crashcourse.week11.facit;

/**
 * Facit: {@code Shape} efter alla fem övningarna. Jämför med
 * {@code com.crashcourse.week11.Shape}; förklaringarna finns i FACIT.md.
 */
public interface Shape {

    double area();

    double perimeter();

    /**
     * Uppgift 3: en default-metod. Alla klasser som implementerar Shape får
     * den automatiskt, även de som inte ärver från AbstractShape.
     */
    default boolean isLargerThan(Shape other) {
        return area() > other.area();
    }
}
