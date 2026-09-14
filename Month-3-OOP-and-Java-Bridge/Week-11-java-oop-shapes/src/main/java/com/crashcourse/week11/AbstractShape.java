package com.crashcourse.week11;

/**
 * Common base for every concrete shape in this project.
 *
 * <p>Unlike {@link Shape}, an abstract class CAN hold real implementation
 * and state, alongside methods it leaves unimplemented for subclasses to
 * fill in. Here, {@code toString()} is genuinely shared logic — every
 * shape should print the same way — so it belongs here once instead of
 * being copy-pasted into {@code Circle}, {@code Rectangle}, and
 * {@code Triangle} separately. {@code area()} and {@code perimeter()}
 * stay abstract because there's no sensible shared formula for them —
 * only each concrete shape knows its own.
 *
 * <p>{@code AbstractShape} itself {@code implements Shape}, so every
 * subclass automatically satisfies the {@code Shape} contract too — that's
 * what lets a {@code List<Shape>} hold {@code Circle}, {@code Rectangle},
 * and {@code Triangle} objects side by side (see {@link ShapeInventory}).
 */
public abstract class AbstractShape implements Shape {

    @Override
    public String toString() {
        return String.format(
                "%s[area=%.4f, perimeter=%.4f]",
                getClass().getSimpleName(), area(), perimeter());
    }
}
