package com.crashcourse.week11;

public class Main {

    public static void main(String[] args) {
        ShapeInventory inventory = new ShapeInventory();
        inventory.add(new Circle(3));
        inventory.add(new Rectangle(4, 5));
        inventory.add(new Triangle(3, 4, 5));

        System.out.println("Shapes sorted by area:");
        for (Shape shape : inventory.sortedByArea()) {
            System.out.println("  " + shape);
        }

        System.out.printf("Total area: %.4f%n", inventory.totalArea());
        System.out.println("Largest: " + inventory.largestByArea());
    }
}
