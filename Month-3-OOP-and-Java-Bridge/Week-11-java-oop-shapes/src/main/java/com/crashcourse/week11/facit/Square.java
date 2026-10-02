package com.crashcourse.week11.facit;

/**
 * Uppgift 1: en kvadrat är en rektangel där bredd och höjd är lika.
 *
 * <p>Konstruktorn skickar samma sida som både bredd och höjd till
 * Rectangle, så area- och omkretsformlerna ärvs i stället för att skrivas
 * en gång till.
 */
public class Square extends Rectangle {

    public Square(double side) {
        super(side, side);
    }

    public double getSide() {
        return getWidth();
    }
}
