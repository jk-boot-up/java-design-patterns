package com.jk.explore.composite;

import java.math.BigDecimal;

/**
 * The trap in full. Because {@link NaiveProduct} and {@link NaiveCategory}
 * share no common type, every single operation on the tree — pricing,
 * counting, printing — has to repeat the exact same {@code instanceof}
 * chain to figure out what it is looking at. Add a third kind of catalog
 * item tomorrow and all three methods below need a new branch, or they
 * silently fall through to the exception at the bottom.
 */
public final class NaiveCatalogPrinter {

    private NaiveCatalogPrinter() {
    }

    public static BigDecimal totalPrice(Object item) {
        if (item instanceof NaiveProduct product) {
            return product.price();
        }
        if (item instanceof NaiveCategory category) {
            BigDecimal sum = BigDecimal.ZERO;
            for (Object child : category.children()) {
                sum = sum.add(totalPrice(child));
            }
            return sum;
        }
        throw new IllegalArgumentException("Unknown catalog item: " + item);
    }

    public static int productCount(Object item) {
        if (item instanceof NaiveProduct) {
            return 1;
        }
        if (item instanceof NaiveCategory category) {
            int count = 0;
            for (Object child : category.children()) {
                count += productCount(child);
            }
            return count;
        }
        throw new IllegalArgumentException("Unknown catalog item: " + item);
    }

    public static void print(Object item, String indent) {
        if (item instanceof NaiveProduct product) {
            System.out.println(indent + "- " + product.name() + " ($" + product.price() + ")");
            return;
        }
        if (item instanceof NaiveCategory category) {
            System.out.println(indent + "+ " + category.name() + "/");
            for (Object child : category.children()) {
                print(child, indent + "  ");
            }
            return;
        }
        throw new IllegalArgumentException("Unknown catalog item: " + item);
    }
}
