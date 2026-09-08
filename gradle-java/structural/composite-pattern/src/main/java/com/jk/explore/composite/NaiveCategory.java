package com.jk.explore.composite;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * The naive composite's other half. A plain holder of children — {@code
 * Object} children, because a {@code NaiveProduct} and a {@code
 * NaiveCategory} have no shared supertype. Every caller that walks this
 * tree has to rediscover, at every level, which kind of {@code Object} it
 * is holding.
 */
public final class NaiveCategory {

    private final String name;
    private final List<Object> children = new ArrayList<>();

    public NaiveCategory(String name) {
        this.name = Objects.requireNonNull(name);
    }

    public NaiveCategory add(Object child) {
        children.add(Objects.requireNonNull(child));
        return this;
    }

    public String name() {
        return name;
    }

    public List<Object> children() {
        return Collections.unmodifiableList(children);
    }
}
