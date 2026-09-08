package com.jk.explore.composite;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * The Composite. Holds any mix of {@link Product} leaves and nested
 * {@code Category} subtrees, and answers every {@link CatalogComponent}
 * question by delegating to its children and combining the results — it
 * never needs to know whether a child is itself a leaf or another
 * composite.
 */
public final class Category implements CatalogComponent {

    private final String name;
    private final List<CatalogComponent> children = new ArrayList<>();

    public Category(String name) {
        this.name = Objects.requireNonNull(name);
    }

    public Category add(CatalogComponent child) {
        children.add(Objects.requireNonNull(child));
        return this;
    }

    public List<CatalogComponent> children() {
        return Collections.unmodifiableList(children);
    }

    @Override
    public String name() {
        return name;
    }

    @Override
    public BigDecimal totalPrice() {
        BigDecimal sum = BigDecimal.ZERO;
        for (CatalogComponent child : children) {
            sum = sum.add(child.totalPrice());
        }
        return sum;
    }

    @Override
    public int productCount() {
        int count = 0;
        for (CatalogComponent child : children) {
            count += child.productCount();
        }
        return count;
    }

    @Override
    public void print(String indent) {
        System.out.println(indent + "+ " + name + "/");
        for (CatalogComponent child : children) {
            child.print(indent + "  ");
        }
    }
}
