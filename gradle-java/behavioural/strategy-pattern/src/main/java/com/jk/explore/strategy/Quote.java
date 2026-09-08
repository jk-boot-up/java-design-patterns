package com.jk.explore.strategy;

import java.util.Objects;

/** What the customer is shown: the rule that applied, and what it cost. */
public record Quote(String ruleName, Money subtotal, Money delivery) {

    public Quote {
        Objects.requireNonNull(ruleName, "ruleName");
        Objects.requireNonNull(subtotal, "subtotal");
        Objects.requireNonNull(delivery, "delivery");
    }

    public Money total() {
        return subtotal.plus(delivery);
    }

    public boolean isFreeDelivery() {
        return delivery.isZero();
    }

    @Override
    public String toString() {
        return String.format("%s: subtotal %s + delivery %s = %s",
                ruleName, subtotal, isFreeDelivery() ? "FREE" : delivery, total());
    }
}
