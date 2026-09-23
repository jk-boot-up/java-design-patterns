package com.jk.explore.deadletterrabbit;

import java.util.HashSet;
import java.util.Set;
import java.util.function.Consumer;

/**
 * The service that does the work on an order. Two things can go wrong, and they are not the same kind of wrong.
 * An address nothing can read fails every time. A payment gateway that timed out fails once and then works.
 */
public class Shipping implements Consumer<Order> {

    private final Set<String> failOnceIds;
    private final Set<String> alreadyFailedOnce = new HashSet<>();
    private boolean addressParserFixed;

    public Shipping(Set<String> failOnceIds) {
        this.failOnceIds = failOnceIds;
    }

    /** What an operator does once the cause of the failure is found and corrected. */
    public void fixTheAddressParser() {
        addressParserFixed = true;
    }

    @Override
    public void accept(Order order) {
        if (order.body().contains("???") && !addressParserFixed) {
            throw new IllegalStateException("cannot read the address of " + order.id());
        }
        if (failOnceIds.contains(order.id()) && alreadyFailedOnce.add(order.id())) {
            throw new IllegalStateException("the payment gateway timed out for " + order.id());
        }
    }
}
