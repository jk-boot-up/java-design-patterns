package com.jk.explore.interpreter;

import java.util.List;

/** Non-terminal expression: any one part matching is enough. */
public record OrRule(List<Rule> parts) implements Rule {

    public OrRule {
        parts = List.copyOf(parts);
    }

    @Override
    public boolean matches(Order order) {
        for (Rule part : parts) {
            if (part.matches(order)) {
                return true;
            }
        }
        return false;
    }

    @Override
    public String describe() {
        return AndRule.join(parts, " or ");
    }
}
