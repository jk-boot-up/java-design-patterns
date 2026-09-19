package com.jk.explore.fluent;

import java.util.Comparator;
import java.util.List;

public class Catalog {

    public static final List<Product> ALL = List.of(
            new Product("Blue Mug", "mugs", 800, true),
            new Product("Big Mug", "mugs", 2400, true),
            new Product("Gift Mug", "mugs", 1900, false),
            new Product("Travel Mug", "mugs", 3200, true),
            new Product("Teapot", "pots", 3500, true),
            new Product("Green Tea", "tea", 400, true));

    /** The version with a long list of positional arguments. */
    public static List<String> find(String category, int maxCents, boolean inStockOnly, boolean sortByPrice, int limit) {
        var stream = ALL.stream()
                .filter(p -> p.category().equals(category))
                .filter(p -> p.priceCents() <= maxCents)
                .filter(p -> !inStockOnly || p.inStock());
        if (sortByPrice) {
            stream = stream.sorted(Comparator.comparingInt(Product::priceCents));
        }
        return stream.limit(limit).map(Product::name).toList();
    }
}
