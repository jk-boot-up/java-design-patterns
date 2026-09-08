package com.jk.explore.visitor;

import java.util.Objects;

/**
 * A single item on the shelf — the Leaf, unchanged from the Composite
 * project apart from the two fields the reports need: how many are in stock,
 * and whether shipping it is restricted.
 *
 * <p>Read the method list. There is a getter for each field, {@code name()}
 * from {@link CatalogComponent}, and {@code accept}. There is nothing here
 * about inventory valuation, nothing about CSV quoting, and nothing about
 * dangerous-goods paperwork, even though this project produces all three
 * reports. That absence is the result being demonstrated; compare it with
 * {@link NaiveProduct}, which carries a method for each.
 */
public final class Product implements CatalogComponent {

    private final String sku;
    private final String name;
    private final Money price;
    private final int stockOnHand;
    private final Restriction restriction;

    public Product(String sku, String name, Money price, int stockOnHand) {
        this(sku, name, price, stockOnHand, Restriction.NONE);
    }

    public Product(String sku, String name, Money price, int stockOnHand,
                   Restriction restriction) {
        this.sku = Objects.requireNonNull(sku, "sku");
        this.name = Objects.requireNonNull(name, "name");
        this.price = Objects.requireNonNull(price, "price");
        if (stockOnHand < 0) {
            throw new IllegalArgumentException("stock cannot be negative: " + stockOnHand);
        }
        this.stockOnHand = stockOnHand;
        this.restriction = Objects.requireNonNull(restriction, "restriction");
    }

    @Override
    public String name() {
        return name;
    }

    public String sku() {
        return sku;
    }

    /** What one of them costs. */
    public Money price() {
        return price;
    }

    /** How many are in the warehouse right now. */
    public int stockOnHand() {
        return stockOnHand;
    }

    public Restriction restriction() {
        return restriction;
    }

    @Override
    public void accept(CatalogVisitor visitor) {
        visitor.visit(this);
    }

    @Override
    public String toString() {
        return name + " (" + sku + ", " + price + " x " + stockOnHand + ")";
    }
}
