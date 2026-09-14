package com.crashcourse.week11;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class RectangleTest {

    private static final double DELTA = 1e-9;

    @Test
    void areaIsWidthTimesHeight() {
        Rectangle rectangle = new Rectangle(4, 5);
        assertEquals(20.0, rectangle.area(), DELTA);
    }

    @Test
    void perimeterIsTwiceWidthPlusHeight() {
        Rectangle rectangle = new Rectangle(4, 5);
        assertEquals(18.0, rectangle.perimeter(), DELTA);
    }

    @Test
    void nonPositiveDimensionsRejected() {
        assertThrows(IllegalArgumentException.class, () -> new Rectangle(0, 5));
        assertThrows(IllegalArgumentException.class, () -> new Rectangle(5, 0));
        assertThrows(IllegalArgumentException.class, () -> new Rectangle(-1, 5));
    }
}
