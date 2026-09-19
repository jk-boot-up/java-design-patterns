package com.jk.explore.delegation.naive;

/** The base of the inheritance version. */
public class PlainOrder {

    private final long subtotalCents;

    public PlainOrder(long subtotalCents) {
        this.subtotalCents = subtotalCents;
    }

    protected long subtotal() {
        return subtotalCents;
    }

    public long total() {
        return subtotalCents;
    }
}
