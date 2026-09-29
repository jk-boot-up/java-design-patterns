package com.jk.explore.higherorder;

import java.util.List;

/**
 * A product in the store's catalogue.
 */
public record Product(String name, String category, double price, int stock) {

    public static List<Product> catalogue() {
        return List.of(
                new Product("Blue mug", "mug", 8.50, 12),
                new Product("Travel mug", "mug", 14.00, 0),
                new Product("Desk lamp", "lamp", 45.00, 3),
                new Product("Mini lamp", "lamp", 9.00, 7),
                new Product("Tea towel", "kitchen", 4.00, 30),
                new Product("Teapot", "kitchen", 22.00, 0));
    }
}
