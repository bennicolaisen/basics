package com.crashcourse.week11;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class TriangleTest {

    private static final double DELTA = 1e-6;

    @Test
    void areaOfThreeFourFiveTriangleIsSix() {
        // A classic right triangle: Heron's formula should give exactly 6.
        Triangle triangle = new Triangle(3, 4, 5);
        assertEquals(6.0, triangle.area(), DELTA);
    }

    @Test
    void perimeterIsSumOfSides() {
        Triangle triangle = new Triangle(3, 4, 5);
        assertEquals(12.0, triangle.perimeter(), DELTA);
    }

    @Test
    void invalidTriangleInequalityRejected() {
        // 1 + 2 is not > 10: these three lengths can't form a triangle.
        assertThrows(IllegalArgumentException.class, () -> new Triangle(1, 2, 10));
    }

    @Test
    void degenerateTriangleRejected() {
        // 1 + 2 == 3 exactly: a degenerate (flat) triangle, still invalid.
        assertThrows(IllegalArgumentException.class, () -> new Triangle(1, 2, 3));
    }

    @Test
    void nonPositiveSideRejected() {
        assertThrows(IllegalArgumentException.class, () -> new Triangle(0, 4, 5));
        assertThrows(IllegalArgumentException.class, () -> new Triangle(3, -4, 5));
    }
}
