package com.jk.explore.delegation.naive;

public class GiftOrder extends PlainOrder {

    private final int items;

    public GiftOrder(long subtotalCents, int items) {
        super(subtotalCents);
        this.items = items;
    }

    @Override
    public long total() {
        return super.total() + 300L * items;
    }
}
