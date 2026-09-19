package com.jk.explore.fluent;

import java.util.Comparator;
import java.util.List;

/** A fluent query that never changes: every call answers with a new query. */
public final class Query {

    private final String category;
    private final int maxCents;
    private final boolean inStockOnly;
    private final boolean sortByPrice;
    private final int limit;

    private Query(String category, int maxCents, boolean inStockOnly, boolean sortByPrice, int limit) {
        this.category = category;
        this.maxCents = maxCents;
        this.inStockOnly = inStockOnly;
        this.sortByPrice = sortByPrice;
        this.limit = limit;
    }

    public static Query search() {
        return new Query(null, Integer.MAX_VALUE, false, false, Integer.MAX_VALUE);
    }

    public Query category(String category) {
        return new Query(category, maxCents, inStockOnly, sortByPrice, limit);
    }

    public Query under(int cents) {
        return new Query(category, cents, inStockOnly, sortByPrice, limit);
    }

    public Query inStock() {
        return new Query(category, maxCents, true, sortByPrice, limit);
    }

    public Query cheapestFirst() {
        return new Query(category, maxCents, inStockOnly, true, limit);
    }

    public Query first(int n) {
        return new Query(category, maxCents, inStockOnly, sortByPrice, n);
    }

    /** The only place that checks anything, so a bad value is found here, far from where it was given. */
    public List<String> run() {
        if (maxCents < 0) {
            throw new IllegalStateException("the price limit is below zero: " + maxCents);
        }
        var stream = Catalog.ALL.stream()
                .filter(p -> category == null || p.category().equals(category))
                .filter(p -> p.priceCents() <= maxCents)
                .filter(p -> !inStockOnly || p.inStock());
        if (sortByPrice) {
            stream = stream.sorted(Comparator.comparingInt(Product::priceCents));
        }
        return stream.limit(limit).map(Product::name).toList();
    }
}
