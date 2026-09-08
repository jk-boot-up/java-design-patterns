package com.jk.explore.composite;

import java.math.BigDecimal;
import java.util.Objects;

/** The Leaf. A single product, with no children of its own. */
public final class Product implements CatalogComponent {

    private final String name;
    private final BigDecimal price;

    public Product(String name, BigDecimal price) {
        this.name = Objects.requireNonNull(name);
        this.price = Objects.requireNonNull(price);
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BigDecimal totalPrice() {
        return price;
    }

    @Override
    public int productCount() {
        return 1;
    }

    @Override
    public void print(String indent) {
        System.out.println(indent + "- " + name + " ($" + price + ")");
    }
}
