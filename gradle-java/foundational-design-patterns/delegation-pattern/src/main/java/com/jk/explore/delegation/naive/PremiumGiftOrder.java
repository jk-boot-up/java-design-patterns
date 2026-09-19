package com.jk.explore.delegation.naive;

/** Needs its own class, because a class can have only one parent. */
public class PremiumGiftOrder extends PremiumOrder {

    private final int items;

    public PremiumGiftOrder(long subtotalCents, int items) {
        super(subtotalCents);
        this.items = items;
    }

    @Override
    public long total() {
        return super.total() + 300L * items;
    }
}
