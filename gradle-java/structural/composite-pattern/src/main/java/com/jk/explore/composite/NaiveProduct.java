package com.jk.explore.composite;

import java.math.BigDecimal;
import java.util.Objects;

/**
 * Attempt one, kept around as the trap. {@code NaiveProduct} and
 * {@link NaiveCategory} share no common type, so nothing can treat them
 * uniformly — every piece of client code has to ask "which one is this?"
 * for itself.
 */
public final class NaiveProduct {

    private final String name;
    private final BigDecimal price;

    public NaiveProduct(String name, BigDecimal price) {
        this.name = Objects.requireNonNull(name);
        this.price = Objects.requireNonNull(price);
    }

    public String name() {
        return name;
    }

    public BigDecimal price() {
        return price;
    }
}
