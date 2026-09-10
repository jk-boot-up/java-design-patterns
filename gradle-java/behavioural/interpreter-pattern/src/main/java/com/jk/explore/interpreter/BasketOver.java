package com.jk.explore.interpreter;

/**
 * Terminal expression: "basket over 50".
 *
 * <p>A terminal is a leaf — it holds no other rule, and answering it is one
 * comparison. Every terminal in this project is this small, on purpose: the
 * interesting behaviour comes from how they are combined, not from any one of
 * them.
 */
public record BasketOver(int pounds) implements Rule {

    @Override
    public boolean matches(Order order) {
        return order.basketPounds() > pounds;
    }

    @Override
    public String describe() {
        return "basket over " + pounds;
    }
}
