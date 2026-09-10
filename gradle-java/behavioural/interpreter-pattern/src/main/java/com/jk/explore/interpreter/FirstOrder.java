package com.jk.explore.interpreter;

/**
 * Terminal expression: "first order".
 *
 * <p>A record with no components, because the rule has nothing to remember.
 * Java still gives it a sensible {@code equals}, which is what lets the tests
 * compare two parsed trees directly.
 */
public record FirstOrder() implements Rule {

    @Override
    public boolean matches(Order order) {
        return order.firstOrder();
    }

    @Override
    public String describe() {
        return "first order";
    }
}
