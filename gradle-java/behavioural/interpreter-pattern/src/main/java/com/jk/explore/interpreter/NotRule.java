package com.jk.explore.interpreter;

/**
 * Non-terminal expression with exactly one part: the opposite of it.
 *
 * <p>Worth reading next to {@link AndRule}: a non-terminal does not have to
 * hold a list. It only has to hold at least one other rule, and to answer by
 * asking.
 */
public record NotRule(Rule part) implements Rule {

    @Override
    public boolean matches(Order order) {
        return !part.matches(order);
    }

    @Override
    public String describe() {
        return "not " + part.describe();
    }
}
