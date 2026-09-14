package com.crashcourse.week11;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class CircleTest {

    private static final double DELTA = 1e-6;

    @Test
    void areaMatchesPiRSquared() {
        Circle circle = new Circle(2);
        assertEquals(Math.PI * 4, circle.area(), DELTA);
    }

    @Test
    void perimeterMatchesTwoPiR() {
        Circle circle = new Circle(2);
        assertEquals(2 * Math.PI * 2, circle.perimeter(), DELTA);
    }

    @Test
    void nonPositiveRadiusRejected() {
        assertThrows(IllegalArgumentException.class, () -> new Circle(0));
        assertThrows(IllegalArgumentException.class, () -> new Circle(-1));
    }

    @Test
    void toStringIncludesClassNameAreaAndPerimeter() {
        Circle circle = new Circle(1);
        String text = circle.toString();
        assertTrue(text.startsWith("Circle["));
        assertTrue(text.contains("area="));
        assertTrue(text.contains("perimeter="));
    }
}
