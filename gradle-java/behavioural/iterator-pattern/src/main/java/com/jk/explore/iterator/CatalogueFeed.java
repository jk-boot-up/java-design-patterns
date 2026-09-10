package com.jk.explore.iterator;

import java.util.ArrayList;
import java.util.List;

/**
 * The shop's product feed, as the warehouse actually exposes it: one page at a
 * time.
 *
 * <p>This is the awkward shape the rest of the example exists to hide. You
 * cannot ask it for "all products" -- you ask for page 0, then page 1, and so
 * on, and you know you have reached the end when a page comes back empty.
 * Real catalogue APIs behave exactly like this, because nobody wants to send
 * forty thousand products in one response.
 *
 * <p>It counts the pages it has handed out. That counter is not decoration:
 * two of the tests use it to prove the catalogue only fetches a page when
 * somebody actually asks for the products on it.
 */
public class CatalogueFeed {

    /** How many products the warehouse puts on one page. */
    public static final int PAGE_SIZE = 3;

    private final List<Product> everything;
    private int pagesFetched;

    public CatalogueFeed(List<Product> everything) {
        this.everything = List.copyOf(everything);
    }

    /**
     * Returns page {@code number}, counting from zero, or an empty list once
     * you have run off the end.
     */
    public List<Product> page(int number) {
        if (number < 0) {
            throw new IllegalArgumentException("page number cannot be negative: " + number);
        }
        pagesFetched++;
        int from = number * PAGE_SIZE;
        if (from >= everything.size()) {
            return List.of();
        }
        int to = Math.min(from + PAGE_SIZE, everything.size());
        return new ArrayList<>(everything.subList(from, to));
    }

    /** How many times {@link #page(int)} has been called. */
    public int pagesFetched() {
        return pagesFetched;
    }

    public int totalProducts() {
        return everything.size();
    }

    /** The catalogue the demo and the tests browse. */
    public static CatalogueFeed sampleShop() {
        return new CatalogueFeed(List.of(
                new Product("SKU-001", "Cotton T-Shirt", "clothing", 12),
                new Product("SKU-002", "Cotton Socks", "clothing", 4),
                new Product("SKU-003", "Wool Scarf", "clothing", 18),
                new Product("SKU-004", "Desk Lamp", "home", 30),
                new Product("SKU-005", "Coffee Mug", "home", 8),
                new Product("SKU-006", "Cushion Cover", "home", 15),
                new Product("SKU-007", "Paperback Novel", "books", 9),
                new Product("SKU-008", "Cookbook", "books", 22)));
    }
}
