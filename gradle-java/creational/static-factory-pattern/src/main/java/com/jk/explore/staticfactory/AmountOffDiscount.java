package com.jk.explore.staticfactory;

/** A flat amount off, capped so it can never exceed the subtotal. */
final class AmountOffDiscount implements Discount {

    private final Money amount;

    AmountOffDiscount(Money amount) {
        this.amount = amount;
    }

    @Override
    public Money appliedTo(Order order) {
        return amount.cappedAt(order.subtotal());
    }

    @Override
    public String describe() {
        return amount + " off";
    }
}
