package com.crashcourse.week15;

/** An immutable catalog item with a fixed, positive base price. */
public final class Item {

    private final String id;
    private final String name;
    private final double basePrice;

    public Item(String id, String name, double basePrice) {
        if (id == null || id.isBlank()) {
            throw new IllegalArgumentException("Item id must not be blank");
        }
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Item name must not be blank");
        }
        if (basePrice < 0) {
            throw new IllegalArgumentException("Base price must not be negative, got " + basePrice);
        }
        this.id = id;
        this.name = name;
        this.basePrice = basePrice;
    }

    public String id() {
        return id;
    }

    public String name() {
        return name;
    }

    public double basePrice() {
        return basePrice;
    }

    @Override
    public String toString() {
        return "Item{id='%s', name='%s', basePrice=%.2f}".formatted(id, name, basePrice);
    }
}
