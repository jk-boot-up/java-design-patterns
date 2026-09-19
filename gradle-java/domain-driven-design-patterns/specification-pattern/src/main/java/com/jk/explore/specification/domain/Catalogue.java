package com.jk.explore.specification.domain;

import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

/** A catalogue held in memory. Every product it looks at is counted. */
public class Catalogue {

    private final List<Product> products;
    private final AtomicInteger examined = new AtomicInteger();

    public Catalogue(List<Product> products) {
        this.products = products;
    }

    public int examined() {
        return examined.get();
    }

    public List<Product> select(Specification<Product> rule) {
        return products.stream().filter(p -> {
            examined.incrementAndGet();
            return rule.isSatisfiedBy(p);
        }).toList();
    }
}
