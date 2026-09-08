package com.jk.explore.visitor;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * A kit sold as one thing — "Starter Kit: phone, case and charger" — at a
 * price of its own.
 *
 * <p>This is the third node type, and it is here because it is what makes
 * the tree interesting to report on. A bundle is not a category: you cannot
 * add its contents up and call that its value, because the whole point of a
 * bundle is that it costs less than its parts. And it is not a product: it
 * has contents, and a compliance report has to look inside them.
 *
 * <p>So every report has to say something different about a bundle than it
 * says about a product. That is exactly the situation Visitor is for, and
 * exactly the situation an {@code instanceof} chain handles by growing a
 * branch in every report — see {@link NaiveBundle}, where the branch was
 * grown by copying the product one, and one copy was not finished.
 */
public final class Bundle implements CatalogComponent {

    private final String sku;
    private final String name;
    private final Money price;
    private final int stockOnHand;
    private final List<Product> contents = new ArrayList<>();

    public Bundle(String sku, String name, Money price, int stockOnHand) {
        this.sku = Objects.requireNonNull(sku, "sku");
        this.name = Objects.requireNonNull(name, "name");
        this.price = Objects.requireNonNull(price, "price");
        this.stockOnHand = stockOnHand;
    }

    /** Fluent, so a kit reads as one expression. */
    public Bundle containing(Product product) {
        contents.add(Objects.requireNonNull(product, "product"));
        return this;
    }

    @Override
    public String name() {
        return name;
    }

    public String sku() {
        return sku;
    }

    /** The kit price — deliberately not the sum of {@link #contents()}. */
    public Money price() {
        return price;
    }

    public int stockOnHand() {
        return stockOnHand;
    }

    /** What is in the box. A report may look; it may not rearrange. */
    public List<Product> contents() {
        return Collections.unmodifiableList(contents);
    }

    /**
     * The saving against buying the parts separately — the reason a bundle
     * cannot be valued by adding its contents up.
     */
    public Money savingAgainstParts() {
        Money parts = Money.zero();
        for (Product product : contents) {
            parts = parts.plus(product.price());
        }
        return parts.minus(price);
    }

    @Override
    public void accept(CatalogVisitor visitor) {
        visitor.visit(this);
    }

    @Override
    public String toString() {
        return name + " (" + sku + ", " + price + ", " + contents.size() + " items)";
    }
}
