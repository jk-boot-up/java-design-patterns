package com.jk.explore.inputvalidation;

/**
 * How many of a product: a whole number from 1 to 99.
 */
public record Quantity(int value) {

    public Quantity {
        if (value < 1 || value > 99) {
            throw new IllegalArgumentException("quantity must be from 1 to 99");
        }
    }

    public static Quantity parse(String text) {
        try {
            return new Quantity(Integer.parseInt(text.trim()));
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("quantity must be a whole number");
        }
    }
}
