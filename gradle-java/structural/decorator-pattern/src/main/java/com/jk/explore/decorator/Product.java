package com.jk.explore.decorator;

import java.math.BigDecimal;
import java.util.Objects;

public final class Product implements PricedItem {

    private final String name;
    private final BigDecimal price;

    public Product(String name, BigDecimal price) {
        this.name = Objects.requireNonNull(name);
        this.price = Objects.requireNonNull(price);
    }

    @Override
    public BigDecimal cost() {
        return price;
    }

    @Override
    public String description() {
        return name;
    }
}
