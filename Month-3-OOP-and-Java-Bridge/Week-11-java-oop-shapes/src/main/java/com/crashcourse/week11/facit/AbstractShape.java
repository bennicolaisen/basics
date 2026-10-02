package com.crashcourse.week11.facit;

/**
 * Facit: {@code AbstractShape}, som nu också är {@code Comparable} efter
 * area (uppgift 4).
 */
public abstract class AbstractShape implements Shape, Comparable<Shape> {

    @Override
    public int compareTo(Shape other) {
        return Double.compare(area(), other.area());
    }

    @Override
    public String toString() {
        return String.format(
                "%s[area=%.4f, perimeter=%.4f]",
                getClass().getSimpleName(), area(), perimeter());
    }
}
