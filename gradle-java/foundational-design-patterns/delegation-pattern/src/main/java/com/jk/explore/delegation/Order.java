package com.jk.explore.delegation;

/** An order that does not price itself. It hands the pricing to a rule, which it can swap. */
public class Order {

    private final long subtotalCents;
    private final int items;
    private PricingRule rule;

    public Order(long subtotalCents, int items, PricingRule rule) {
        this.subtotalCents = subtotalCents;
        this.items = items;
        this.rule = rule;
    }

    public long subtotalCents() {
        return subtotalCents;
    }

    public int itemCount() {
        return items;
    }

    public void useRule(PricingRule rule) {
        this.rule = rule;
    }

    /** Delegates: the rule does the work, and is given the order so that it can look at it. */
    public long total() {
        return rule.adjust(subtotalCents, this);
    }
}
