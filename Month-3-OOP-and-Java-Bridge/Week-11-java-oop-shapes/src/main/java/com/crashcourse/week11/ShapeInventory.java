package com.crashcourse.week11;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.NoSuchElementException;

/**
 * Holds a collection of shapes and aggregates over them entirely through
 * the {@link Shape} interface — it never needs to know whether a given
 * element is a {@link Circle}, {@link Rectangle}, or {@link Triangle}.
 */
public class ShapeInventory {

    private final List<Shape> shapes = new ArrayList<>();

    public void add(Shape shape) {
        if (shape == null) {
            throw new IllegalArgumentException("shape must not be null");
        }
        shapes.add(shape);
    }

    public int size() {
        return shapes.size();
    }

    public double totalArea() {
        double total = 0.0;
        for (Shape shape : shapes) {
            total += shape.area(); // polymorphic call: dispatched to each shape's real class
        }
        return total;
    }

    public Shape largestByArea() {
        return shapes.stream()
                .max(Comparator.comparingDouble(Shape::area))
                .orElseThrow(() -> new NoSuchElementException("inventory is empty"));
    }

    /** Returns a new list sorted by area, ascending — the internal list is never mutated. */
    public List<Shape> sortedByArea() {
        List<Shape> copy = new ArrayList<>(shapes);
        copy.sort(Comparator.comparingDouble(Shape::area));
        return copy;
    }
}
