package com.crashcourse.week11.facit;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.NoSuchElementException;

/** Facit: ShapeInventory efter uppgift 2, 4 och 5. Se FACIT.md. */
public class ShapeInventory {

    private static final Comparator<Shape> BY_AREA = Comparator.comparingDouble(Shape::area);

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
            total += shape.area();
        }
        return total;
    }

    /** Uppgift 5: samma sak som totalArea, med en stream. */
    public double totalAreaWithStream() {
        return shapes.stream().mapToDouble(Shape::area).sum();
    }

    /** Uppgift 2: largest och smallest delar på en hjälpmetod. */
    public Shape largestByArea() {
        return extremeByArea(BY_AREA);
    }

    public Shape smallestByArea() {
        return extremeByArea(BY_AREA.reversed());
    }

    private Shape extremeByArea(Comparator<Shape> order) {
        return shapes.stream()
                .max(order)
                .orElseThrow(() -> new NoSuchElementException("inventory is empty"));
    }

    /** Ny lista sorterad efter area, med en Comparator. Den interna listan ändras aldrig. */
    public List<Shape> sortedByArea() {
        List<Shape> copy = new ArrayList<>(shapes);
        copy.sort(BY_AREA);
        return copy;
    }

    /**
     * Uppgift 4: sortera med formernas naturliga ordning (compareTo i
     * AbstractShape) i stället för en Comparator.
     */
    public static List<AbstractShape> sortedNaturally(List<AbstractShape> shapes) {
        List<AbstractShape> copy = new ArrayList<>(shapes);
        Collections.sort(copy);
        return copy;
    }
}
