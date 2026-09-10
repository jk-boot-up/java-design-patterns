package com.jk.explore.interpreter;

/** Terminal expression: "items at least 3". */
public record ItemsAtLeast(int count) implements Rule {

    @Override
    public boolean matches(Order order) {
        return order.itemCount() >= count;
    }

    @Override
    public String describe() {
        return "items at least " + count;
    }
}
