package com.crashcourse.week11;

/**
 * A triangle defined by its three side lengths. Area is computed with
 * Heron's formula, so no angles or coordinates are needed.
 */
public class Triangle extends AbstractShape {

    private final double sideA;
    private final double sideB;
    private final double sideC;

    public Triangle(double sideA, double sideB, double sideC) {
        if (sideA <= 0 || sideB <= 0 || sideC <= 0) {
            throw new IllegalArgumentException("all sides must be > 0");
        }
        // Triangle inequality: each side must be shorter than the sum of
        // the other two, or the three lengths can't actually close into a
        // triangle at all.
        if (sideA + sideB <= sideC || sideA + sideC <= sideB || sideB + sideC <= sideA) {
            throw new IllegalArgumentException(
                    "sides " + sideA + ", " + sideB + ", " + sideC
                            + " violate the triangle inequality");
        }
        this.sideA = sideA;
        this.sideB = sideB;
        this.sideC = sideC;
    }

    @Override
    public double area() {
        double s = perimeter() / 2.0; // semi-perimeter
        return Math.sqrt(s * (s - sideA) * (s - sideB) * (s - sideC));
    }

    @Override
    public double perimeter() {
        return sideA + sideB + sideC;
    }
}
