package com.jk.explore.interpreter;

import java.util.List;

/**
 * Non-terminal expression: every part must match.
 *
 * <p>This is where the pattern actually happens. The class knows two things —
 * that all of its parts must agree, and how to ask a part — and it knows
 * nothing else. It does not know what its parts are, how many levels are below
 * it, or whether they are leaves or more {@code AndRule}s, because it never has
 * to look.
 */
public record AndRule(List<Rule> parts) implements Rule {

    public AndRule {
        parts = List.copyOf(parts);
    }

    @Override
    public boolean matches(Order order) {
        for (Rule part : parts) {
            if (!part.matches(order)) {
                return false;
            }
        }
        return true;
    }

    @Override
    public String describe() {
        return join(parts, " and ");
    }

    /** Shared by both non-terminals: each part describes itself, in order. */
    static String join(List<Rule> parts, String separator) {
        StringBuilder text = new StringBuilder();
        for (Rule part : parts) {
            if (text.length() > 0) {
                text.append(separator);
            }
            text.append(part.describe());
        }
        return text.toString();
    }
}
