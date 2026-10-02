package com.crashcourse.week11.facit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.NoSuchElementException;
import org.junit.jupiter.api.Test;

class FacitTest {

    @Test
    void squareIsARectangleWithEqualSides() {
        Square square = new Square(3);
        assertEquals(9.0, square.area(), 1e-9);
        assertEquals(12.0, square.perimeter(), 1e-9);
        assertEquals(3.0, square.getSide(), 1e-9);
        assertInstanceOf(Rectangle.class, square);
    }

    @Test
    void squareRejectsNonPositiveSide() {
        assertThrows(IllegalArgumentException.class, () -> new Square(0));
    }

    @Test
    void inventoryHandlesSquaresWithoutAnyChange() {
        ShapeInventory inventory = new ShapeInventory();
        inventory.add(new Square(2));
        inventory.add(new Rectangle(1, 3));
        assertEquals(7.0, inventory.totalArea(), 1e-9);
    }

    @Test
    void smallestAndLargestByArea() {
        ShapeInventory inventory = new ShapeInventory();
        Shape small = new Square(1);
        Shape large = new Circle(2);
        inventory.add(new Rectangle(2, 3));
        inventory.add(small);
        inventory.add(large);
        assertSame(small, inventory.smallestByArea());
        assertSame(large, inventory.largestByArea());
    }

    @Test
    void emptyInventoryHasNoSmallest() {
        assertThrows(NoSuchElementException.class, () -> new ShapeInventory().smallestByArea());
    }

    @Test
    void defaultMethodCompareAreas() {
        assertTrue(new Circle(2).isLargerThan(new Square(1)));
        assertFalse(new Square(1).isLargerThan(new Square(1)));
    }

    @Test
    void defaultMethodWorksForShapesOutsideTheClassHierarchy() {
        Shape unitShape = new Shape() {
            @Override
            public double area() {
                return 1.0;
            }

            @Override
            public double perimeter() {
                return 4.0;
            }
        };
        assertTrue(new Square(2).isLargerThan(unitShape));
        assertFalse(unitShape.isLargerThan(new Square(2)));
    }

    @Test
    void naturalOrderingIsByArea() {
        AbstractShape big = new Square(3);
        AbstractShape small = new Square(1);
        AbstractShape middle = new Rectangle(1, 4);
        List<AbstractShape> sorted = ShapeInventory.sortedNaturally(List.of(big, small, middle));
        assertEquals(List.of(small, middle, big), sorted);
    }

    @Test
    void streamTotalMatchesLoopTotal() {
        ShapeInventory inventory = new ShapeInventory();
        inventory.add(new Circle(1));
        inventory.add(new Triangle(3, 4, 5));
        inventory.add(new Square(2));
        assertEquals(inventory.totalArea(), inventory.totalAreaWithStream(), 1e-9);
        assertEquals(0.0, new ShapeInventory().totalAreaWithStream(), 0.0);
    }
}
