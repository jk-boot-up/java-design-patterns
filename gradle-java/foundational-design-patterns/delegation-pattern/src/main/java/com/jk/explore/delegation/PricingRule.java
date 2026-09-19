package com.jk.explore.delegation;

import java.util.concurrent.atomic.AtomicInteger;

/** The delegate: takes a running total and the order, and returns the new total. */
public interface PricingRule {

    AtomicInteger CALLS = new AtomicInteger();

    long adjust(long cents, Order order);

    PricingRule NONE = (cents, order) -> {
        CALLS.incrementAndGet();
        return cents;
    };

    static PricingRule premium() {
        return (cents, order) -> {
            CALLS.incrementAndGet();
            return cents - cents / 10;
        };
    }

    /** Three hundred cents for each item in the order, so it needs to see the order. */
    static PricingRule giftWrap() {
        return (cents, order) -> {
            CALLS.incrementAndGet();
            return cents + 300L * order.itemCount();
        };
    }

    /** Applies each rule in turn. */
    static PricingRule inOrder(PricingRule... rules) {
        return (cents, order) -> {
            long total = cents;
            for (PricingRule r : rules) {
                total = r.adjust(total, order);
            }
            return total;
        };
    }
}
