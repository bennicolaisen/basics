package com.crashcourse.week11;

/**
 * A geometric shape that can report its own area and perimeter.
 *
 * <p>An interface is a pure contract: it declares *what* every
 * implementing class must be able to do, with zero implementation and no
 * state of its own. Any class, regardless of what it already extends,
 * can promise to fulfill this contract by writing {@code implements
 * Shape}. That's the point of using an interface here rather than a
 * class: {@code Circle}, {@code Rectangle}, and {@code Triangle} share
 * nothing about *how* they compute area or perimeter, but they all agree
 * on *that* they can.
 */
public interface Shape {

    double area();

    double perimeter();
}
