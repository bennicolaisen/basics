package com.crashcourse.week11;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import java.util.NoSuchElementException;
import org.junit.jupiter.api.Test;

class ShapeInventoryTest {

    private static final double DELTA = 1e-6;

    @Test
    void totalAreaSumsAllShapes() {
        ShapeInventory inventory = new ShapeInventory();
        Rectangle rectangle = new Rectangle(2, 3); // area 6
        Circle circle = new Circle(1); // area pi
        inventory.add(rectangle);
        inventory.add(circle);

        assertEquals(6.0 + Math.PI, inventory.totalArea(), DELTA);
    }

    @Test
    void largestByAreaReturnsBiggestShape() {
        ShapeInventory inventory = new ShapeInventory();
        Rectangle small = new Rectangle(1, 1); // area 1
        Rectangle large = new Rectangle(10, 10); // area 100
        inventory.add(small);
        inventory.add(large);

        assertSame(large, inventory.largestByArea());
    }

    @Test
    void largestByAreaOnEmptyInventoryThrows() {
        ShapeInventory inventory = new ShapeInventory();
        assertThrows(NoSuchElementException.class, inventory::largestByArea);
    }

    @Test
    void sortedByAreaReturnsAscendingCopyWithoutMutatingInternalOrder() {
        ShapeInventory inventory = new ShapeInventory();
        Rectangle large = new Rectangle(10, 10); // area 100
        Rectangle small = new Rectangle(1, 1); // area 1
        inventory.add(large);
        inventory.add(small);

        List<Shape> sorted = inventory.sortedByArea();
        assertSame(small, sorted.get(0));
        assertSame(large, sorted.get(1));

        // Internal insertion order is untouched: largestByArea still finds
        // `large` correctly regardless of what sortedByArea() returned.
        assertSame(large, inventory.largestByArea());
    }

    @Test
    void addingNullShapeRejected() {
        ShapeInventory inventory = new ShapeInventory();
        assertThrows(IllegalArgumentException.class, () -> inventory.add(null));
    }

    @Test
    void polymorphismSumsAreaThroughSharedInterfaceReference() {
        // Every element here is stored and iterated as `Shape` — the
        // interface reference — even though each is a different concrete
        // class. shape.area() dispatches to the right implementation at
        // runtime for each one (dynamic dispatch).
        List<Shape> shapes = List.of(
                new Circle(2),
                new Rectangle(3, 4),
                new Triangle(3, 4, 5));

        double total = 0.0;
        for (Shape shape : shapes) {
            total += shape.area();
        }

        double expected = (Math.PI * 4) + 12.0 + 6.0;
        assertEquals(expected, total, DELTA);
    }
}
